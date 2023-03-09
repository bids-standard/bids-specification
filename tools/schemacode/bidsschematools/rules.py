import re
import typing as ty
from collections.abc import Mapping
from functools import lru_cache

import bidsschematools as bst
import bidsschematools.types

# The list of which entities create directories could be dynamically specified by the YAML, but for
# now, it is not.
# Ordering is important, as "subject" follows "session" alphabetically, but is hierarchically
# above it.
DIR_ENTITIES = ["subject", "session"]


def _capture_regex(name, pattern, backref):
    """Capture pattern to name or match back-reference to name

    >>> _capture_regex("run", "[0-9]+", False)
    '(?P<run>[0-9]+)'
    >>> _capture_regex("run", "[0-9]+", True)
    '(?P=run)'
    >>> re.match(_capture_regex("run", "[0-9]+", False), "123_").groupdict()
    {'run': '123'}
    """
    return f"(?P={name})" if backref else f"(?P<{name}>{pattern})"


def _optional_regex(regex, optional):
    """Return an optional version of a regex if optional is True

    A required regex is passed through unchanged:

    >>> pattern = _optional_regex("xyz", False)
    >>> pattern
    'xyz'
    >>> re.match(pattern, "xyz").groups()
    ()
    >>> re.match(pattern, "") is None
    True

    An optional regex uses a non-capturing group, to avoid interfering
    with existing groups

    >>> pattern = _optional_regex("x(?P<name>[a-z])z", True)
    >>> pattern
    '(?:x(?P<name>[a-z])z)?'
    >>> re.match(pattern, "xyz").groups()
    ('y',)
    >>> re.match(pattern, "xyz").groupdict()
    {'name': 'y'}
    >>> re.match(pattern, "").groups()
    (None,)
    >>> re.match(pattern, "").groupdict()
    {'name': None}
    """
    return f"(?:{regex})?" if optional else regex


@lru_cache()
def _format_entity(entity, name, pattern, level, directory=False):
    if directory and entity not in DIR_ENTITIES:
        return ""

    label = _capture_regex(entity, pattern, not directory and entity in DIR_ENTITIES)
    post = "/" if directory else "_"

    return _optional_regex(f"{name}-{label}{post}", level != "required")


def _entity_rule(rule: Mapping, schema: bst.types.Namespace):
    dir_regex = []
    entity_regex = []
    for ent in schema.rules.entities:
        if ent not in rule["entities"]:
            continue
        ent_obj = rule["entities"][ent]
        if isinstance(ent_obj, str):
            ent_obj = {"level": ent_obj}
        # Allow filename rule to override original entity fields
        entity = {**schema.objects.entities[ent], **ent_obj}

        if "enum" in entity:
            pattern = "|".join(entity["enum"])
        else:
            pattern = schema.objects.formats[entity["format"]].pattern

        dir_regex.append(
            _format_entity(ent, entity["name"], pattern, entity["level"], directory=True)
        )
        entity_regex.append(_format_entity(ent, entity["name"], pattern, entity["level"]))

    dtypes = set(rule.get("datatypes", ()))
    optional_dtype = "" in dtypes
    if optional_dtype:
        dtypes.remove("")
    if dtypes:
        pattern = f"(?P<datatype>{'|'.join(dtypes)})/"
        if optional_dtype:
            pattern = f"(?:{pattern})?"
        dir_regex += pattern

    # If we move to referring to suffixes by keys in the object table:
    # suffixes = [schema.objects.suffixes[suffix].value for suffix in rule["suffixes"]]
    suffixes = rule["suffixes"]
    suffix_regex = f"(?P<suffix>{'|'.join(suffixes)})"

    # If we move to referring to extensions by keys in the object table:
    # extensions = [schema.objects.extensions[ext].value for ext in rule["extensions"]]
    extensions = rule["extensions"]
    ext_match = "|".join(_sanitize_extension(ext) for ext in extensions)
    ext_regex = f"(?P<extension>{ext_match})"

    return {
        "regex": "".join(dir_regex + entity_regex + [suffix_regex, ext_regex]),
        "mandatory": False,
    }


def _split_inheritance_rules(rule: Mapping) -> ty.List[Mapping]:
    """Break composite rules into main and sidecar rules

    Implements the inheritance principle for file naming.
    """
    heritable_exts = {".tsv", ".json", ".bval", ".bvec"}
    rule_exts = set(rule["extensions"])

    main_exts = rule_exts - heritable_exts
    # If a rule only has TSV or JSON files, entities can be
    # made required
    if not main_exts:
        if ".tsv" in rule_exts:
            main_exts = {".tsv"}
        elif ".json" in rule_exts:
            main_exts = {".json"}

    sidecar_exts = rule_exts - main_exts
    if not sidecar_exts:
        return [rule]

    sidecar_dtypes = [""] + rule.get("datatypes", [])
    sidecar_entities = {ent: "optional" for ent in rule["entities"]}

    main_rule = {**rule, **{"extensions": list(main_exts)}}
    sidecar_rule = {
        **rule,
        **{
            "extensions": list(sidecar_exts),
            "datatypes": sidecar_dtypes,
            "entities": sidecar_entities,
        },
    }

    return [main_rule, sidecar_rule]


def _sanitize_extension(ext: str) -> str:
    if ext == ".*":
        return r"\.[a-zA-Z0-9.]+"
    return re.escape(ext)


def _stem_rule(rule: bst.types.Namespace):
    stem_regex = re.escape(rule.stem)
    ext_match = "|".join(_sanitize_extension(ext) for ext in rule.extensions)
    ext_regex = f"(?P<extension>{ext_match})"

    return {"regex": stem_regex + ext_regex, "mandatory": rule.level == "required"}


def _path_rule(rule: bst.types.Namespace):
    return {"regex": re.escape(rule.path), "mandatory": rule.level == "required"}


def regexify_filename_rules(
    rule_group: bst.types.Namespace,
    schema: bst.types.Namespace,
    level: int,
):
    """Load schema rules into regular expressions

    Parameters
    ----------
    rule_group : Namespace
        The set of rules to load from the schema
    schema : Namespace
        A nested dictionary, as returned by `bidsschematools.schema.load_schema()`.
    level : int
        The depth in rule_group to look for rules

    Returns
    -------
    rules : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """
    regex_schema = []
    for rule_template in rule_group.values(level=level):
        # Simple rules, e.g. dataset_description.json, README
        if "path" in rule_template:
            regex_schema.append(_path_rule(rule_template))
        elif "stem" in rule_template:
            regex_schema.append(_stem_rule(rule_template))
        else:
            regex_schema.extend(
                _entity_rule(rule, schema) for rule in _split_inheritance_rules(rule_template)
            )

    return regex_schema


@lru_cache()
def regexify_all(schema_dir=None):
    """
    Create full path regexes for all BIDS specification files.

    Parameters
    ----------
    schema_dir : str, optional
        A string pointing to a BIDS directory for which paths should be validated.

    Returns
    -------
    all_regex : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    my_schema : Mapping
        Nested dictionaries representing the full schema.
    """

    schema = bst.schema.load_schema(schema_dir)
    all_regex = []
    for group in (schema.rules.files.common, schema.rules.files.raw):
        all_regex.extend(regexify_filename_rules(group, schema, level=2))

    return all_regex, schema

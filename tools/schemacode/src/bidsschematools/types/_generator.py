from __future__ import annotations

import json

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any


PRELUDE = '''\
"""BIDS validation context definitions

The classes in this module are used to define the context for BIDS validation.
The context is a namespace that contains relevant information about the dataset
as a whole and an individual file to be validated.

These classes are used to define the structure of the context,
but they cannot be instantiated directly.
Conforming subtypes need only match the structure of these classes,
and do not need to inherit from them.

The classes use ``@property`` decorators to indicate that subtypes need only
provide read access to the attributes, and may restrict writing, for example,
when calculating attributes dynamically based on other attributes.

Note that some type checkers will not match classes that use
:class:`functools.cached_property`.
To permit this, add the following to your module::

    if TYPE_CHECKING:
        cached_property = property
    else:
        from functools import cached_property

This module has been auto-generated from the BIDS schema version {version}.
"""

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Mapping, Sequence
    from typing import Any, Literal, Protocol
else:
    Any = object
    Literal = tuple
    Mapping = dict
    Protocol = object
    Sequence = list

__all__ = {__all__}


'''

CLASS = '''\
class {name}(Protocol):
    """{docstring}"""
'''

ATTR = '''\
    @property
    def {name}(self) -> {type}:
        """{docstring}"""
'''


def snake_to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def create_protocol_source(
    class_name: str,
    properties: dict[str, Any],
    metadata: dict[str, Any],
    protocols: dict[str, str],
) -> str:
    class_name = snake_to_pascal(class_name)
    lines = [CLASS.format(name=class_name, docstring=metadata.get("description", "").strip())]
    for prop_name, prop_info in properties.items():
        type_, md = typespec_to_source(prop_name, prop_info, protocols)
        lines.append(
            ATTR.format(name=prop_name, type=type_, docstring=md.get("description", "").strip())
        )

    protocols[class_name] = "\n".join(lines)
    return class_name


def typespec_to_source(
    name: str,
    typespec: dict[str, Any],
    protocols: dict[str, str],
) -> tuple[str, dict[str, Any]]:
    """Convert JSON-schema style specification to type and metadata dictionary."""
    tp = typespec.get("type")
    if not tp:
        raise ValueError(f"Invalid typespec: {json.dumps(typespec)}")
    metadata = {key: typespec[key] for key in ("name", "description") if key in typespec}
    if tp == "object":
        properties = typespec.get("properties")
        if properties:
            type_ = create_protocol_source(
                name, properties=properties, metadata=metadata, protocols=protocols
            )
        else:
            type_ = "Mapping[str, Any]"
    elif tp == "array":
        if "items" in typespec:
            subtype, md = typespec_to_source(name, typespec["items"], protocols=protocols)
        else:
            subtype = "Any"
        type_ = f"Sequence[{subtype}]"
    else:
        type_ = {
            "number": "float",
            "string": "str",
            "integer": "int",
        }[tp]
        if type_ == "str" and "enum" in typespec:
            type_ = f"Literal[{', '.join(f'{v!r}' for v in typespec['enum'])}]"
    return type_, metadata


def generate_protocols(typespec: dict[str, Any], root_class_name: str) -> dict[str, str]:
    """Generate protocol definitions from a JSON schema typespec."""
    protocols: dict[str, str] = {}
    typespec_to_source(root_class_name, typespec, protocols)
    return protocols


def generate_module(schema: dict[str, Any]) -> str:
    """Generate a context module source code from a BIDS schema.

    Returns a tuple containing the module source code and a list of protocol names.
    """
    protocols = generate_protocols(schema["meta"]["context"], "context")
    prelude = PRELUDE.format(version=schema["schema_version"], __all__=list(protocols))
    return prelude + "\n\n".join(protocols.values())

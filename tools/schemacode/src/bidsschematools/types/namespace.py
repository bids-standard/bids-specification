"""Namespace types

The purpose of the :class:`~Namespace` type is to make a directory of
YAML files available as a single dictionary and allow attribute (``.``)
lookups.
"""

import json
import typing as ty
from collections.abc import ItemsView, KeysView, Mapping, MutableMapping, ValuesView
from pathlib import Path

import yaml


def _expand_dots(entry: ty.Tuple[str, ty.Any]) -> ty.Tuple[str, ty.Any]:
    # Helper function for expand
    key, val = entry
    if "." in key:
        init, post = key.split(".", 1)
        return init, dict([_expand_dots((post, val))])
    return key, expand(val)


def expand(element):
    """Expand a dict, recursively, to replace dots in keys with recursive dictionaries

    Parameters
    ----------
    element : dict
        The dictionary to expand

    Returns
    -------
    dict :
        The expanded dictionary

    Examples
    --------
    >>> expand({"a": 1, "b.c": 2, "d": [{"e": 3, "f.g": 4}]})
    {'a': 1, 'b': {'c': 2}, 'd': [{'e': 3, 'f': {'g': 4}}]}
    """
    if isinstance(element, dict):
        return {key: val for key, val in map(_expand_dots, element.items())}
    elif isinstance(element, list):
        return [expand(el) for el in element]
    return element


class NsItemsView(ItemsView):
    def __init__(self, namespace, level):
        self._mapping = namespace
        self._level = level

    def __contains__(self, item):
        key, val = item
        keys = key.split(".", self._level - 1)
        if "." in keys[-1]:
            return False
        return self._mapping[key] == val

    def __iter__(self):
        l1 = ItemsView(self._mapping)
        if self._level == 1:
            yield from l1
        else:
            yield from (
                (f"{key}.{subkey}", subval)
                for key, val in l1
                # Items/keys/values can only be found in namespaces
                # ignore lists and scalars
                if isinstance(val, Mapping)
                for subkey, subval in NsItemsView(val, self._level - 1)
            )


class NsKeysView(KeysView):
    def __init__(self, namespace, level):
        self._mapping = namespace
        self._level = level

    def __contains__(self, key):
        keys = key.split(".", self._level - 1)
        if "." in keys[-1]:
            return False
        return key in self._mapping

    def __iter__(self):
        yield from (key for key, val in NsItemsView(self._mapping, self._level))


class NsValuesView(ValuesView):
    def __init__(self, namespace, level):
        self._mapping = namespace
        self._level = level
        self._items = NsItemsView(namespace, level)

    def __contains__(self, val):
        return any(val == item[1] for item in self._items)

    def __iter__(self):
        yield from (val for key, val in self._items)


class Namespace(MutableMapping):
    """Provides recursive attribute style access to a dict-like structure

    Examples
    --------
    >>> ns = Namespace.build({"a": 1, "b.c": "val"})
    >>> ns.a
    1
    >>> ns["a"]
    1
    >>> ns.b
    <Namespace {'c': 'val'}>
    >>> ns["b"]
    <Namespace {'c': 'val'}>
    >>> ns.b.c
    'val'
    >>> ns["b.c"]
    'val'
    >>> ns["b"]["c"]
    'val'
    >>> ns.b["c"]
    'val'
    >>> ns["b"].c
    'val'

    ``.keys()``, ``.values()`` and ``.items()`` can take an optional ``level`` argument:

    >>> list(ns.keys())
    ['a', 'b']
    >>> list(ns.keys(level=2))
    ['b.c']
    >>> 'b.c' in ns.keys()
    False
    >>> 'b.c' in ns.keys(level=2)
    True

    >>> list(ns.values())
    [1, <Namespace {'c': 'val'}>]
    >>> list(ns.values(level=2))
    ['val']
    >>> 'val' in ns.values()
    False
    >>> 'val' in ns.values(level=2)
    True

    >>> list(ns.items())
    [('a', 1), ('b', <Namespace {'c': 'val'}>)]
    >>> list(ns.items(level=2))
    [('b.c', 'val')]
    >>> ("b.c", "val") in ns.items()
    False
    >>> ("b.c", "val") in ns.items(level=2)
    True

    >>> ns["d.e.f"] = "val2"
    >>> ns.d.e
    <Namespace {'f': 'val2'}>
    >>> ns.d.e.f
    'val2'
    >>> del ns['d']
    """

    def __init__(self, *args, **kwargs):
        self._properties = dict(*args, **kwargs)

    def to_dict(self) -> dict:

        def _to_dict(obj):
            if isinstance(obj, Namespace):
                return {k: _to_dict(v) for k, v in obj._properties.items()}
            if isinstance(obj, list):
                return [_to_dict(v) for v in obj]
            if isinstance(obj, dict):
                return {k: _to_dict(v) for k, v in obj.items()}
            return obj

        return _to_dict(self)

    def __deepcopy__(self, memo):
        return self.build(self.to_dict())

    @classmethod
    def view(cls, mapping):
        if isinstance(mapping, cls):
            return mapping
        if not isinstance(mapping, dict):
            raise ValueError("Namespace.view can only be made from a dict")
        new = cls()
        new._properties = mapping
        return new

    @classmethod
    def build(cls, mapping):
        """Expand mapping recursively and return as namespace"""
        return cls(expand(mapping))

    def items(self, *, level=1) -> NsItemsView:
        return NsItemsView(self, level)

    def keys(self, *, level=1) -> NsKeysView:
        return NsKeysView(self, level)

    def values(self, *, level=1) -> NsValuesView:
        return NsValuesView(self, level)

    def __getattribute__(self, key):
        # Return actual properties first
        err = None
        try:
            return super().__getattribute__(key)
        except AttributeError as e:
            err = e

        # Utilize __getitem__ but keep original error on failure
        try:
            return self[key]
        except KeyError:
            raise err

    def _get_mapping(self, key: str) -> ty.Tuple[Mapping, str]:
        subkeys = key.split(".")
        mapping = self._properties
        for subkey in subkeys[:-1]:
            mapping = mapping.setdefault(subkey, {})
            mapping = getattr(mapping, "_properties", mapping)
            if not isinstance(mapping, Mapping):
                raise KeyError(f"{key} (subkey={subkey})")
        return mapping, subkeys[-1]

    def __getitem__(self, key):
        mapping, subkey = self._get_mapping(key)
        val = mapping[subkey]
        if isinstance(val, dict):
            val = self.view(val)
        return val

    def __setitem__(self, key, val):
        mapping, subkey = self._get_mapping(key)
        mapping[subkey] = val

    def __delitem__(self, key):
        mapping, subkey = self._get_mapping(key)
        del mapping[subkey]

    def __repr__(self):
        return f"<Namespace {self._properties}>"

    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        return iter(self._properties)

    @classmethod
    def from_directory(cls, path, fmt="yaml"):
        if fmt == "yaml":
            return cls.build(_read_yaml_dir(Path(path)))
        raise NotImplementedError(f"Unknown format: {fmt}")

    def to_json(self, **kwargs) -> str:
        return json.dumps(self, cls=MappingEncoder, **kwargs)

    @classmethod
    def from_json(cls, jsonstr: str):
        return cls.build(json.loads(jsonstr))


def _read_yaml_dir(path: Path) -> dict:
    mapping = {}
    for subpath in sorted(path.iterdir()):
        if subpath.is_dir():
            mapping[subpath.name] = _read_yaml_dir(subpath)
        elif subpath.name.endswith("yaml"):
            try:
                mapping[subpath.stem] = yaml.safe_load(subpath.read_text())
            except Exception as e:
                raise ValueError(f"There was an error reading the file: {subpath}") from e
    return mapping


class MappingEncoder(json.JSONEncoder):
    def default(self, o):
        try:
            return super().default(o)
        except TypeError as e:
            err = e
        if isinstance(o, Mapping):
            return dict(o)
        raise err

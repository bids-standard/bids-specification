"""Namespace types"""
from collections.abc import ItemsView, KeysView, Mapping, ValuesView
from pathlib import Path

import yaml


def _expand_dots(entry):
    # Helper function for expand
    key, val = entry
    if "." in key:
        init, post = key.split(".", 1)
        return init, dict([_expand_dots((post, val))])
    return key, expand(val)


def expand(element):
    """Expand a dict, recursively, to replace dots in keys with recursive dictionaries

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


class Namespace(Mapping):
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
    """

    def __init__(self, *args, **kwargs):
        self._properties = dict(*args, **kwargs)

    def to_dict(self):
        ret = {}
        for key, val in self._properties.items():
            if isinstance(val, Namespace):
                val = val.to_dict()
            ret[key] = val
        return ret

    def __deepcopy__(self, memo):
        return self.build(self.to_dict())

    @classmethod
    def build(cls, mapping):
        """Expand mapping recursively and return as namespace"""
        return cls(expand(mapping))

    def items(self, *, level=1):
        return NsItemsView(self, level)

    def keys(self, *, level=1):
        return NsKeysView(self, level)

    def values(self, *, level=1):
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

    def __getitem__(self, key):
        key, dot, subkey = key.partition(".")
        val = self._properties[key]
        if isinstance(val, dict):
            val = self.__class__(val)
        if dot:
            # Recursive step
            val = val[subkey]
        return val

    def __repr__(self):
        return f"<Namespace {self._properties}>"

    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        return iter(self._properties)

    @classmethod
    def from_directory(cls, path, fmt="yaml"):
        mapping = {}
        fullpath = Path(path)
        if fmt == "yaml":
            for subpath in sorted(fullpath.iterdir()):
                if subpath.is_dir():
                    submapping = cls.from_directory(subpath)
                    if submapping:
                        mapping[subpath.name] = submapping
                elif subpath.name.endswith("yaml"):
                    mapping[subpath.stem] = yaml.safe_load(subpath.read_text())
            return cls.build(mapping)
        raise NotImplementedError(f"Unknown format: {fmt}")

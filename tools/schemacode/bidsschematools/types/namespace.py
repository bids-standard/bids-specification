"""Namespace types"""
from collections.abc import Mapping
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

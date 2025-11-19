"""BIDS validation context code generator

This module produces source code for BIDS validation context classes.
The source code can be executed at import time to ensure that classes
are consistent with the current state of the BIDS schema.

When packaging, calling modules should be replaced with the source code
they execute, ensuring that the classes are available for static analysis
and can be compiled to bytecode.

This module can be removed during packaging.
"""

from __future__ import annotations

import json
from textwrap import dedent, indent

TYPE_CHECKING = False
if TYPE_CHECKING:
    from collections.abc import Mapping
    from typing import Any, Callable, Protocol

    class Spec(Protocol):
        prelude: str
        class_def: str
        attr_def: str
        proto_prefix: str


def with_indent(spaces: int, /) -> Callable[[str], str]:
    def decorator(attr: str) -> str:
        return indent(dedent(attr), " " * spaces)

    return decorator


class ProtocolSpec:
    prelude = dedent('''\
    """BIDS validation context definitions

    The classes in this module are used to define the context for BIDS validation.
    The context is a namespace that contains relevant information about the dataset
    as a whole and an individual file to be validated.

    These classes are used to define the structure of the context,
    but they cannot be instantiated directly.
    Conforming subtypes need only match the structure of these classes,
    and do not need to inherit from them.
    It is recommended to import this module in an ``if TYPE_CHECKING`` block
    to avoid import costs.

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

    from __future__ import annotations

    from collections.abc import Mapping, Sequence
    from typing import Any, Literal, Protocol

    __all__ = {__all__}


    ''')

    class_def = dedent('''\
    class {name}(Protocol):
        """{docstring}"""
    ''')

    attr_def = with_indent(4)('''\
        @property
        def {name}(self) -> {type}:
            """{docstring}"""
    ''')

    proto_prefix = ""


class DataclassSpec:
    prelude = dedent('''\
    """BIDS validation context dataclasses

    The classes in this module may be used to populate the context for BIDS validation.

    This module has been auto-generated from the BIDS schema version {version}.
    """

    from __future__ import annotations

    import sys
    from dataclasses import dataclass

    TYPE_CHECKING = False
    if TYPE_CHECKING or "sphinx.ext.autodoc" in sys.modules:
        from collections.abc import Mapping, Sequence
        from typing import Any, Literal

        from . import protocols

    if sys.version_info >= (3, 10):
        dc_kwargs = {{"slots": True, "frozen": True}}
    else:  # PY39
        dc_kwargs = {{"frozen": True}}

    __all__ = {__all__}


    ''')

    class_def = dedent('''\
    @dataclass(**dc_kwargs)
    class {name}:
        """{docstring}"""
    ''')

    attr_def = with_indent(4)("""\
        {name}: {type}{default}
        #: {docstring}
    """)

    proto_prefix = "protocols."


def snake_to_pascal(name: str) -> str:
    return "".join(word.capitalize() for word in name.split("_"))


def create_protocol_source(
    class_name: str,
    properties: dict[str, Any],
    metadata: dict[str, Any],
    template: Spec,
    classes: dict[str, str],
) -> str:
    class_name = snake_to_pascal(class_name)
    docstring = metadata.get("description", "").strip()
    if "@property" not in template.attr_def:
        docstring += with_indent(4)("""

            Attributes
            ----------
            """)

    required = metadata.get("required", {})
    optional = [prop for prop in properties if prop not in required]

    lines = []
    for prop_name in (*required, *optional):
        prop_info = properties[prop_name]
        type_, md = typespec_to_source(prop_name, prop_info, template, classes)
        default = ""
        if prop_name not in required:
            type_ = f"{type_} | None"
            default = " = None"
        if not type_.startswith(("int", "float", "str", "bool", "Literal", "Sequence", "Mapping")):
            type_ = f"{template.proto_prefix}{type_}"
        description = md.get("description", "").strip()
        lines.append(
            template.attr_def.format(
                name=prop_name, type=type_, docstring=description, default=default
            )
        )
        # Avoid double-documenting properties
        if "@property" not in template.attr_def:
            docstring += with_indent(4)(f"""\
                {prop_name}: {type_}
                    {description}

                """)

    lines.insert(0, template.class_def.format(name=class_name, docstring=docstring))

    classes[class_name] = "\n".join(lines)
    return class_name


def typespec_to_source(
    name: str,
    typespec: dict[str, Any],
    template: Spec,
    classes: dict[str, str],
) -> tuple[str, dict[str, Any]]:
    """Convert JSON-schema style specification to type and metadata dictionary."""
    tp = typespec.get("type")
    if not tp:
        raise ValueError(f"Invalid typespec: {json.dumps(typespec)}")
    metadata = {
        key: typespec[key] for key in ("name", "description", "required") if key in typespec
    }
    if tp == "object":
        properties = typespec.get("properties")
        if properties:
            type_ = create_protocol_source(
                name, properties=properties, metadata=metadata, template=template, classes=classes
            )
        else:
            type_ = "Mapping[str, Any]"
    elif tp == "array":
        if "items" in typespec:
            subtype, md = typespec_to_source(name, typespec["items"], template, classes=classes)
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


def generate_protocols(
    typespec: dict[str, Any],
    root_class_name: str,
    template: Spec,
) -> dict[str, str]:
    """Generate protocol definitions from a JSON schema typespec."""
    protocols: dict[str, str] = {}
    typespec_to_source(
        root_class_name,
        typespec,
        template=template,
        classes=protocols,
    )
    return protocols


def generate_module(schema: Mapping[str, Any], class_type: str) -> str:
    """Generate a context module source code from a BIDS schema.

    Returns a tuple containing the module source code and a list of protocol names.
    """
    template: Spec = ProtocolSpec if class_type == "protocol" else DataclassSpec
    protocols = generate_protocols(schema["meta"]["context"], "context", template)
    prelude = template.prelude.format(version=schema["schema_version"], __all__=list(protocols))
    return prelude + "\n\n".join(protocols.values())

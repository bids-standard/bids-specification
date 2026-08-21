from __future__ import annotations

import io
import re

import pandas as pd
from markdown_it import MarkdownIt
from tabulate import tabulate

from ..utils import WarningsFilter, in_context
from .utils import propagate_fence_exception


@propagate_fence_exception
@in_context(WarningsFilter(("error",)))
def fence(
    source: str,
    language: str,
    css_class: str,
    options: dict,
    md,
    classes: list[str],
    id_value="",
    attrs: dict | None = None,
    **kwargs,
) -> str:
    attrs = attrs or {}
    linenums = attrs.get("linenums", "0") == "1"

    if language == "tsvgz" and "header" not in attrs:
        attrs["noheader"] = True

    classes[:0] = ["tsv-table", "index" if linenums else "noindex"]

    df = pd.read_csv(
        io.StringIO(source),
        sep="\t",
        dtype=str,
        index_col=False,
        keep_default_na=False,
        header=None if "noheader" in attrs else "infer",
    )
    md_table = tabulate(
        df,  # type: ignore
        tablefmt="github",
        showindex=linenums,
        headers="keys",
        numalign="right",
    )
    html = MarkdownIt("commonmark").enable("table").render(md_table)
    if "noheader" in attrs:
        html = re.sub("<thead>.+</thead>", "", html, flags=re.DOTALL)

    html = html.replace("<table>", f'<table class="{" ".join(classes)}">')

    # Remove newlines from HTML to prevent copy-paste from inserting spaces
    return html.replace("\n", "")

from __future__ import annotations

import io
import re

import pandas as pd
from markdown_it import MarkdownIt
from tabulate import tabulate


def fence(
    source: str,
    language: str,
    css_class: str,
    options: dict,
    md,
    classes=None,
    id_value="",
    attrs: dict | None = None,
    **kwargs,
) -> str:
    attrs = attrs or {}
    linenums = attrs.get("linenums", "0") == "1"

    if language == "tsvgz" and "header" not in attrs:
        attrs["noheader"] = True

    classes = classes or []
    classes.insert(0, "tsv-table")
    classes.insert(1, "index" if linenums else "noindex")

    try:
        df = pd.read_csv(
            io.StringIO(source),
            sep="\t",
            dtype=str,
            index_col=False,
            keep_default_na=False,
            header=None if "noheader" in attrs else "infer",
        )
        md_table = tabulate(
            df,
            tablefmt="github",
            showindex=linenums,
            headers="keys",
            numalign="right",
        )  # type: ignore
        html = MarkdownIt("commonmark").enable("table").render(md_table)
        if "noheader" in attrs:
            html = re.sub("<thead>.+</thead>", "", html, flags=re.DOTALL)

        if classes:
            html = html.replace("<table>", f'<table class="{" ".join(classes)}">')

        # Remove newlines from HTML to prevent copy-paste from inserting spaces
        return html.replace("\n", "")
    except Exception:
        import traceback

        exc = traceback.format_exc()
        return f"<pre>{exc}</pre>"

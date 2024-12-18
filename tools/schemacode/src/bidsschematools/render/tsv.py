import io

import pandas as pd
from markdown_it import MarkdownIt
from tabulate import tabulate


def fence(source: str, language: str, css_class: str, options: dict, md, **kwargs) -> str:
    try:
        df = pd.read_csv(io.StringIO(source), sep="\t", dtype=str, keep_default_na=False)
        md_table = tabulate(df, headers="keys", tablefmt="github", showindex=False)  # type: ignore
        html = MarkdownIt("commonmark").enable("table").render(md_table)
        # Remove newlines from HTML to prevent copy-paste from inserting spaces
        return html.replace("\n", "")
    except Exception:
        import traceback

        exc = traceback.format_exc()
        return f"<pre>{exc}</pre>"

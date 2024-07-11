from __future__ import annotations

import io
import typing as ty

import pandas as pd
from tabulate import tabulate

if ty.TYPE_CHECKING:
    import markdown


def fence(
    source: str,
    language: str,
    css_class: str,
    options: dict,
    md: markdown.Markdown,
    **kwargs,
) -> str:
    print(f"{source=}")
    print(f"{language=}")
    print(f"{css_class=}")
    print(f"{options=}")
    print(f"{md=}")
    print(f"{kwargs=}")
    try:
        df = pd.read_csv(io.StringIO(source), sep="\t")
        print(df)
        md_table = tabulate(df, headers="keys", tablefmt="github", showindex=False)  # type: ignore
        print(md_table)
        ret = md.convert(md_table)
        print(ret)
        # Remove newlines to prevent copy-paste from inserting spaces
        return ret.replace("\n", "")
    except Exception:
        import traceback

        exc = traceback.format_exc()
        print(exc)
        return f"<pre>{exc}</pre>"

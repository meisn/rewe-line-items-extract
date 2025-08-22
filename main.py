import datetime
import json
import pathlib
import re

import cyclopts
import pymupdf


def text_from_pdf(file: pathlib.Path) -> str:
    """Extracts text from a PDF file.

    Args:
        file (pathlib.Path): Path to the PDF file.

    Returns:
        str: Extracted text from the PDF, joined by form feed characters.
    """
    with pymupdf.open(file) as document:
        text = chr(12).join([page.get_text(sort=True) for page in document])  # type: ignore
    return text


def extract_line_items(text: str) -> list[dict[str, float]]:
    """Extracts line items from a given text.

    Args:
        text (str): Text extracted from a PDF.

    Returns:
        list[dict[str, float]]: Result Dictionary with article names and their costs.
    """
    pattern = re.compile(r"^(?P<article>\w+)\s+(?P<cost>[\d,]+) B$", re.MULTILINE)

    res = []
    for line in text.splitlines():
        if mtch := pattern.search(line):
            item = mtch.groupdict()
            item["cost"] = float(item["cost"].replace(",", "."))
            res.append(item)
    return res


app = cyclopts.App()


@app.default
def extract_line_items_from_pdf(file: pathlib.Path) -> None:
    """Extracts line items from a PDF file and prints them.

    Args:
        file (pathlib.Path): Path to the PDF file.
    """
    file_stat = file.stat()
    print(f"File size: {file_stat.st_size} bytes")
    print(
        f"Last modified: {datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat()}"
    )
    time_suffix = datetime.datetime.fromtimestamp(file.stat().st_birthtime).strftime(
        "%Y%m%d_%H%M%S"
    )

    text = text_from_pdf(file)
    items = extract_line_items(text)
    for item in items:
        print(f"{item['article']}: {item['cost']:.2f} B")

    out_file = file.with_stem(f"{file.stem}_{time_suffix}_items").with_suffix(".json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)
    print(f"Line items saved to {out_file}")


if __name__ == "__main__":
    app()

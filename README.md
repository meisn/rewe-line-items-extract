# REWE Line Items Extract

This small script tries to extract line items from an electronic receipt.

## Dependencies
- [Cyclopts](https://github.com/BrianPugh/cyclopts)
- [PyMuPDF](https://github.com/pymupdf/PyMuPDF)

## Usage

The script utilises a single command only and requires a single pdf file as parameter.

```ps
PS D:\git\rewe-line-items-extract> uv run .\main.py ".\REWE-eBon.pdf"
File size: 27362 bytes
Last modified: 2025-08-22T13:43:11.650330
BACONWUERFEL: 1.59 B
ZWIEBEL: 0.33 B
Line items saved to .\REWE-eBon_20250822_134311_items.json
``` 

The script is build using `cyclopts` and would print some nice help and formatted errors.
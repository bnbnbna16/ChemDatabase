# ChemDatabase

A minimal ChemDraw viewer/tagger prototype.

## Features

- Opens ChemDraw `.cdxml` files (and `.cdx` files if they contain CDXML text)
- Draws atoms and bonds on a canvas
- Lets you click each chemical atom and attach a custom tag
- Lists all assigned tags in a sidebar

## Run

```bash
python cdx_tagger.py
```

Or open a file directly:

```bash
python cdx_tagger.py /absolute/path/to/file.cdxml
```

## Test

```bash
python -m unittest discover -s tests
```

> Note: Binary ChemDraw `.cdx` files are not directly parseable in this prototype. Exporting from ChemDraw as `.cdxml` provides full drawing and tagging support.

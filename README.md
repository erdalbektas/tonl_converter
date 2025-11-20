# TONL Converter

A Python library for converting to and from [TONL](https://github.com/erdalbektas/tonl_converter) (Token-Optimized Notation Language).

## Features

- Convert JSON, YAML, and Markdown tables to TONL.
- Convert TONL to JSON, YAML, and Markdown.
- CLI tool for easy file conversion.
- Token-optimized output format.

## Installation

```bash
pip install tonl-converter
```

## Usage

### CLI

```bash
# Convert JSON to TONL
tonl input.json output.tonl

# Convert TONL to JSON
tonl input.tonl output.json

# Convert to Markdown table
tonl data.tonl report.md
```

### Python API

```python
from tonl_converter import load, dump, to_json, from_json

# Load TONL file
with open('data.tonl', 'r') as f:
    data = load(f)

# Convert to JSON
json_str = to_json(data)
```

## License

MIT

# Villa Ecommerce SDK Documentation

This directory contains all documentation for the Villa Ecommerce SDK.

## Structure

```
docs/
├── api/                    # API reference documentation
│   └── python.md           # Python API reference
├── guides/                 # Usage guides and tutorials
│   └── python-getting-started.md
├── examples/               # Code examples
│   └── python/            # Python examples
├── aws-setup/             # AWS infrastructure setup guides
└── serve_docs.py          # Local documentation server
```

## Viewing Documentation Locally

### Option 1: Using the Documentation Server (Recommended)

Start the local documentation server:

```bash
# From project root
python docs/serve_docs.py

# Or use the convenience script
./docs/start_docs.sh
```

Then open your browser to:
- http://localhost:8000/ (or http://localhost:8001/ if 8000 is in use)

The server provides:
- ✅ Beautiful HTML rendering of markdown files
- ✅ Sidebar navigation
- ✅ Syntax highlighting for code blocks
- ✅ Table of contents
- ✅ Responsive design

### Option 2: Using Python's HTTP Server

For a simple file browser:

```bash
cd docs
python3 -m http.server 8000
```

Then navigate to http://localhost:8000/ in your browser.

### Option 3: Using MkDocs (Advanced)

If you prefer MkDocs:

```bash
pip install mkdocs mkdocs-material
mkdocs serve
```

## Documentation Files

### Python SDK

- **[Python Manual](../python/MANUAL.md)** - Complete Python SDK manual (1,300+ lines)
- **[Python Getting Started](guides/python-getting-started.md)** - Quick start guide
- **[Python API Reference](api/python.md)** - Detailed API documentation

### AWS Setup

- **[AWS Setup README](aws-setup/README.md)** - Overview of AWS setup
- **[Quick Setup](aws-setup/QUICK_SETUP.md)** - Quick reference
- **[Troubleshooting](aws-setup/TROUBLESHOOTING.md)** - Common issues and solutions

### Examples

- **[Basic Usage](../docs/examples/python/basic-usage.py)** - Basic SDK usage examples
- **[Advanced Filtering](../docs/examples/python/advanced-filtering.py)** - Filtering examples
- **[Data Analysis](../docs/examples/python/data-analysis.py)** - Data analysis examples

## Contributing to Documentation

When adding or updating documentation:

1. **Use Markdown** - All docs should be in `.md` format
2. **Follow Structure** - Keep files organized in appropriate directories
3. **Include Examples** - Add code examples where relevant
4. **Update Index** - Update this README if adding new sections
5. **Test Locally** - Use the local server to preview changes

## Documentation Standards

- Use clear, descriptive headings
- Include code examples with proper syntax highlighting
- Link between related documents
- Keep language-specific docs in appropriate directories
- Maintain consistent formatting

## Quick Links

- [Python SDK Manual](../python/MANUAL.md)
- [Python Getting Started](guides/python-getting-started.md)
- [API Reference](api/python.md)
- [AWS Setup Guide](aws-setup/README.md)


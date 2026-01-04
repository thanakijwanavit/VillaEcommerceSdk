#!/usr/bin/env python3
"""
Build static HTML files from markdown documentation for Amplify deployment.
"""

import os
import sys
from pathlib import Path
import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc
import shutil

# Get project root and docs directory
PROJECT_ROOT = Path(__file__).parent.parent
DOCS_DIR = PROJECT_ROOT / 'docs'
DIST_DIR = PROJECT_ROOT / 'dist'
PYTHON_MANUAL = PROJECT_ROOT / 'python' / 'MANUAL.md'

# HTML template (same as serve_docs.py)
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - Villa Ecommerce SDK</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            min-height: 100vh;
        }}
        .sidebar {{
            width: 250px;
            background: #2c3e50;
            color: white;
            padding: 20px;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
        }}
        .sidebar h2 {{
            margin-bottom: 20px;
            font-size: 1.2em;
            border-bottom: 2px solid #34495e;
            padding-bottom: 10px;
        }}
        .sidebar ul {{
            list-style: none;
        }}
        .sidebar li {{
            margin: 5px 0;
        }}
        .sidebar a {{
            color: #ecf0f1;
            text-decoration: none;
            display: block;
            padding: 8px;
            border-radius: 4px;
            transition: background 0.3s;
        }}
        .sidebar a:hover {{
            background: #34495e;
        }}
        .sidebar a.active {{
            background: #3498db;
        }}
        .content {{
            flex: 1;
            margin-left: 250px;
            background: white;
            padding: 40px;
            box-shadow: -2px 0 10px rgba(0,0,0,0.1);
        }}
        .content h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
            margin-bottom: 30px;
        }}
        .content h2 {{
            color: #34495e;
            margin-top: 40px;
            margin-bottom: 20px;
            border-bottom: 2px solid #ecf0f1;
            padding-bottom: 10px;
        }}
        .content h3 {{
            color: #555;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .content code {{
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        .content pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            margin: 20px 0;
        }}
        .content pre code {{
            background: transparent;
            padding: 0;
            color: inherit;
        }}
        .content table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        .content table th,
        .content table td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        .content table th {{
            background: #3498db;
            color: white;
        }}
        .content table tr:nth-child(even) {{
            background: #f9f9f9;
        }}
        .breadcrumb {{
            margin-bottom: 20px;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .breadcrumb a {{
            color: #3498db;
            text-decoration: none;
        }}
        .breadcrumb a:hover {{
            text-decoration: underline;
        }}
        @media (max-width: 768px) {{
            .sidebar {{
                width: 100%;
                height: auto;
                position: relative;
            }}
            .content {{
                margin-left: 0;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            {sidebar}
        </div>
        <div class="content">
            <div class="breadcrumb">{breadcrumb}</div>
            {content}
        </div>
    </div>
</body>
</html>"""

INDEX_CONTENT = """
<h1>Villa Ecommerce SDK Documentation</h1>
<p>Welcome to the Villa Ecommerce SDK documentation. Select a document from the sidebar to get started.</p>

<h2>Quick Links</h2>
<ul>
    <li><a href="/python/MANUAL.html">Python SDK Manual</a> - Complete guide to using the Python SDK</li>
    <li><a href="/guides/python-getting-started.html">Python Getting Started</a> - Quick start guide</li>
    <li><a href="/api/python.html">Python API Reference</a> - API documentation</li>
    <li><a href="/aws-setup/README.html">AWS Setup Guide</a> - AWS configuration</li>
</ul>

<h2>Documentation Structure</h2>
<ul>
    <li><strong>Python SDK</strong> - Complete Python SDK documentation</li>
    <li><strong>Guides</strong> - Step-by-step tutorials and guides</li>
    <li><strong>API Reference</strong> - Detailed API documentation</li>
    <li><strong>AWS Setup</strong> - AWS infrastructure setup guides</li>
    <li><strong>Examples</strong> - Code examples and use cases</li>
</ul>
"""

def generate_sidebar(current_path):
    """Generate sidebar navigation."""
    items = []
    
    sections = [
        ('Python SDK', '/python/MANUAL.html'),
        ('Getting Started', '/guides/python-getting-started.html'),
        ('API Reference', '/api/python.html'),
        ('AWS Setup', '/aws-setup/README.html'),
    ]
    
    items.append('<h2>📚 Documentation</h2>')
    items.append('<ul>')
    for name, url in sections:
        active = 'active' if current_path == url else ''
        items.append(f'<li><a href="{url}" class="{active}">{name}</a></li>')
    items.append('</ul>')
    
    return '\n'.join(items)

def extract_title(md_content, file_path):
    """Extract title from markdown content."""
    title = file_path.stem.replace('-', ' ').title()
    lines = md_content.split('\n')
    for line in lines[:10]:
        stripped = line.strip()
        if stripped.startswith('# '):
            title = stripped.replace('# ', '').strip()
            break
        elif stripped.startswith('## ') and title == file_path.stem.replace('-', ' ').title():
            title = stripped.replace('## ', '').strip()
            break
    
    if not title or title.strip() == '':
        title = file_path.stem.replace('-', ' ').title()
    
    return title

def generate_breadcrumb(path):
    """Generate breadcrumb navigation."""
    parts = path.strip('/').split('/')
    breadcrumb_parts = ['<a href="/">Home</a>']
    
    current_path = ''
    for i, part in enumerate(parts):
        if part.endswith('.html'):
            part = part.replace('.html', '')
        current_path += '/' + part
        if i < len(parts) - 1:
            breadcrumb_parts.append(f'<a href="{current_path}.html">{part}</a>')
        else:
            breadcrumb_parts.append(part)
    
    return ' / '.join(breadcrumb_parts)

def fix_links_in_html(html_content, current_path):
    """Fix markdown links to point to .html files."""
    import re
    
    # Replace markdown-style links in HTML (e.g., href="file.md" -> href="file.html")
    html_content = re.sub(r'<a href="([^"]+\.md)">([^<]+)</a>', 
                          lambda m: f'<a href="{m.group(1)[:-3]}.html">{m.group(2)}</a>', 
                          html_content)
    
    return html_content

def convert_markdown_to_html(md_file, output_file, relative_path):
    """Convert a markdown file to HTML."""
    print(f"Converting {md_file} -> {output_file}")
    
    with open(md_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert markdown to HTML
    md = markdown.Markdown(
        extensions=['codehilite', 'fenced_code', 'tables', 'toc']
    )
    html_content = md.convert(md_content)
    
    # Fix links to point to .html files
    html_content = fix_links_in_html(html_content, relative_path)
    
    # Generate sidebar
    sidebar = generate_sidebar(relative_path)
    
    # Generate breadcrumb
    breadcrumb = generate_breadcrumb(relative_path)
    
    # Extract title
    title = extract_title(md_content, Path(md_file))
    
    # Generate HTML
    html = HTML_TEMPLATE.format(
        title=title,
        sidebar=sidebar,
        breadcrumb=breadcrumb,
        content=html_content
    )
    
    # Write output
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

def build_index():
    """Build the index page."""
    print("Building index page...")
    index_file = DIST_DIR / 'index.html'
    
    sidebar = generate_sidebar('/')
    breadcrumb = '<a href="/">Home</a>'
    
    html = HTML_TEMPLATE.format(
        title="Villa Ecommerce SDK Documentation",
        sidebar=sidebar,
        breadcrumb=breadcrumb,
        content=INDEX_CONTENT
    )
    
    index_file.parent.mkdir(parents=True, exist_ok=True)
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(html)

def find_markdown_files():
    """Find all markdown files to convert."""
    md_files = []
    
    # Find markdown files in docs directory
    for md_file in DOCS_DIR.rglob('*.md'):
        # Get relative path from docs directory
        rel_path = md_file.relative_to(DOCS_DIR)
        # Convert to HTML path
        html_path = rel_path.with_suffix('.html')
        md_files.append((md_file, html_path))
    
    # Add Python manual
    if PYTHON_MANUAL.exists():
        html_path = Path('python') / 'MANUAL.html'
        md_files.append((PYTHON_MANUAL, html_path))
    
    return md_files

def main():
    """Main build function."""
    print("Starting static site build...")
    
    # Clean dist directory
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True)
    
    # Build index page
    build_index()
    
    # Find and convert all markdown files
    md_files = find_markdown_files()
    
    for md_file, html_path in md_files:
        output_file = DIST_DIR / html_path
        relative_path = '/' + str(html_path).replace('\\', '/')
        convert_markdown_to_html(md_file, output_file, relative_path)
    
    print(f"\n✅ Build complete! Output in {DIST_DIR}")
    print(f"   Built {len(md_files) + 1} pages")

if __name__ == '__main__':
    main()


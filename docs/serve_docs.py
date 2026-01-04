#!/usr/bin/env python3
"""
Simple documentation server for Villa Ecommerce SDK.
Serves markdown documentation files locally with a nice HTML interface.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path
from urllib.parse import unquote
import markdown
from markdown.extensions import codehilite, fenced_code, tables, toc

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

# HTML template
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
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.9em;
        }}
        .content pre {{
            background: #2c3e50;
            color: #ecf0f1;
            padding: 20px;
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
        .content blockquote {{
            border-left: 4px solid #3498db;
            padding-left: 20px;
            margin: 20px 0;
            color: #666;
            font-style: italic;
        }}
        .content ul, .content ol {{
            margin: 20px 0;
            padding-left: 30px;
        }}
        .content li {{
            margin: 10px 0;
        }}
        .content a {{
            color: #3498db;
            text-decoration: none;
        }}
        .content a:hover {{
            text-decoration: underline;
        }}
        .breadcrumb {{
            margin-bottom: 20px;
            color: #666;
            font-size: 0.9em;
        }}
        .breadcrumb a {{
            color: #3498db;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="sidebar">
            <h2>📚 Documentation</h2>
            {sidebar}
        </div>
        <div class="content">
            <div class="breadcrumb">
                <a href="/">Home</a> / {breadcrumb}
            </div>
            {content}
        </div>
    </div>
</body>
</html>
"""

INDEX_CONTENT = """<h1>Villa Ecommerce SDK Documentation</h1>
<p>Welcome to the Villa Ecommerce SDK documentation. Select a document from the sidebar to get started.</p>

<h2>Quick Links</h2>
<ul>
    <li><a href="/python/MANUAL.md">Python SDK Manual</a> - Complete guide to using the Python SDK</li>
    <li><a href="/guides/python-getting-started.md">Python Getting Started</a> - Quick start guide</li>
    <li><a href="/api/python.md">Python API Reference</a> - API documentation</li>
    <li><a href="/aws-setup/README.md">AWS Setup Guide</a> - AWS configuration</li>
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

class DocsHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Set docs_root to project root, files are in docs/ subdirectory
        self.docs_root = Path(__file__).parent.parent
        self.docs_dir = self.docs_root / 'docs'
        super().__init__(*args, directory=str(self.docs_root), **kwargs)
    
    def do_GET(self):
        path = unquote(self.path)
        
        # Handle root
        if path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            sidebar = self.generate_sidebar('/')
            content = INDEX_CONTENT
            html = HTML_TEMPLATE.format(
                title="Villa Ecommerce SDK Documentation",
                sidebar=sidebar,
                breadcrumb="Home",
                content=content
            )
            self.wfile.write(html.encode())
            return
        
        # Handle markdown files
        if path.endswith('.md'):
            # Remove leading slash and handle both /docs/... and direct paths
            clean_path = path.lstrip('/')
            # If path starts with 'docs/', remove it (we'll add it back)
            if clean_path.startswith('docs/'):
                clean_path = clean_path[5:]  # Remove 'docs/' prefix
            
            # Try docs directory first, then project root
            file_path = self.docs_dir / clean_path
            if not (file_path.exists() and file_path.is_file()):
                # Try project root (for files like python/MANUAL.md)
                file_path = self.docs_root / clean_path
            
            if file_path.exists() and file_path.is_file():
                with open(file_path, 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                # Convert markdown to HTML
                md = markdown.Markdown(
                    extensions=['codehilite', 'fenced_code', 'tables', 'toc']
                )
                html_content = md.convert(md_content)
                
                # Generate sidebar
                sidebar = self.generate_sidebar(path)
                
                # Generate breadcrumb
                parts = path.strip('/').split('/')
                breadcrumb = ' / '.join([f'<a href="/{"/".join(parts[:i+1])}">{part}</a>' 
                                        for i, part in enumerate(parts)])
                
                # Get title from first heading or filename
                title = file_path.stem.replace('-', ' ').title()
                # Try to extract title from markdown (look for first H1 heading)
                lines = md_content.split('\n')
                for line in lines[:10]:  # Check first 10 lines
                    stripped = line.strip()
                    if stripped.startswith('# '):
                        title = stripped.replace('# ', '').strip()
                        break
                    elif stripped.startswith('## ') and title == file_path.stem.replace('-', ' ').title():
                        # Use first H2 if no H1 found and we're still using default title
                        title = stripped.replace('## ', '').strip()
                        break
                
                # Ensure title is not empty
                if not title or title.strip() == '':
                    title = file_path.stem.replace('-', ' ').title()
                
                html = HTML_TEMPLATE.format(
                    title=title,
                    sidebar=sidebar,
                    breadcrumb=breadcrumb,
                    content=html_content
                )
                
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(html.encode())
                return
        
        # Fallback to default handler
        super().do_GET()
    
    def generate_sidebar(self, current_path):
        """Generate sidebar navigation."""
        items = []
        
        # Main sections - paths relative to root (files are in docs/ subdirectory)
        sections = [
            ('Python SDK', '/python/MANUAL.md'),
            ('Getting Started', '/guides/python-getting-started.md'),
            ('API Reference', '/api/python.md'),
            ('AWS Setup', '/aws-setup/README.md'),
        ]
        
        items.append('<ul>')
        for name, url in sections:
            active = 'active' if current_path == url else ''
            items.append(f'<li><a href="{url}" class="{active}">{name}</a></li>')
        
        items.append('</ul>')
        
        return '\n'.join(items)

def main():
    # Start with port 8001 to avoid conflicts with other services
    PORT = 8001
    
    # Check if port is available by trying to bind
    import socket
    for port in range(8001, 8010):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(('', port))
            sock.close()
            PORT = port
            break
        except OSError:
            sock.close()
            continue
    else:
        print("❌ Could not find an available port (8001-8009)")
        return
    
    Handler = DocsHandler
    
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"🚀 Documentation server running at http://localhost:{PORT}/")
        print(f"📚 Serving documentation from: {Path(__file__).parent.parent}")
        print(f"\nPress Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n👋 Server stopped.")

if __name__ == '__main__':
    main()


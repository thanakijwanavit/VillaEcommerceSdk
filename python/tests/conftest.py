"""Pytest configuration to ensure imports work correctly."""
import sys
from pathlib import Path

# Add the src directory to Python path so villa_ecommerce_sdk can be imported
python_dir = Path(__file__).parent.parent
src_dir = python_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))


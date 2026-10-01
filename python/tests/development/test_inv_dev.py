"""Development test file for inventory."""
import sys
from pathlib import Path

# Add src directory to Python path so imports work when running directly
test_file_dir = Path(__file__).parent
python_dir = test_file_dir.parent.parent
src_dir = python_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from villa_ecommerce_sdk.client import VillaClient


def test_import():
    """Test that VillaClient can be imported."""
    assert VillaClient is not None


if __name__ == "__main__":
    # Run pytest programmatically when script is executed directly
    import pytest
    pytest.main([__file__, "-v"])
    client = VillaClient()
    inventory = client.get_inventory(branch=1000)
    print(inventory)
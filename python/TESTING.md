# Testing Guide

This guide explains how to run tests for the Villa Ecommerce SDK.

## Prerequisites

Install the package and development dependencies:

```bash
cd python

# Install the package in development mode
pip install -e .

# Install development dependencies (pytest, pytest-cov, etc.)
pip install -e ".[dev]"
```

Or install dependencies directly:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

## Running Tests

### Run All Tests

```bash
cd python
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Tests with Coverage Report

```bash
pytest --cov=villa_ecommerce_sdk --cov-report=html
```

This will:
- Run all tests
- Generate a coverage report
- Create an HTML coverage report in `htmlcov/index.html`

### Run Specific Test File

```bash
# Test client functionality
pytest tests/test_client.py

# Test products service
pytest tests/test_products.py

# Test inventory service
pytest tests/test_inventory.py

# Test cache functionality
pytest tests/test_cache.py

# Test integration
pytest tests/test_integration.py
```

### Run Specific Test Class or Function

```bash
# Run a specific test class
pytest tests/test_client.py::TestVillaClient

# Run a specific test function
pytest tests/test_client.py::TestVillaClient::test_init

# Run tests matching a pattern
pytest -k "test_init"
```

### Run Tests with Detailed Output

```bash
# Show print statements
pytest -s

# Show local variables on failure
pytest -l

# Show full traceback
pytest --tb=long
```

### Run Tests in Parallel (if pytest-xdist is installed)

```bash
pip install pytest-xdist
pytest -n auto
```

## Test Structure

```
python/tests/
├── __init__.py
├── test_cache.py          # S3Cache tests
├── test_client.py         # VillaClient tests
├── test_integration.py   # Integration tests
├── test_inventory.py     # InventoryService tests
└── test_products.py      # ProductsService tests
```

## Writing New Tests

When adding new functionality, create corresponding tests:

1. **Test file naming**: `test_<module_name>.py`
2. **Test class naming**: `Test<ClassName>`
3. **Test function naming**: `test_<function_name>`

Example:

```python
import pytest
from villa_ecommerce_sdk.payments import PaymentService

class TestPaymentService:
    """Test cases for PaymentService."""
    
    def test_create_payment(self):
        """Test payment creation."""
        # Your test code here
        pass
```

## Continuous Integration

Tests should pass before committing. The project uses pytest with the following configuration (from `pyproject.toml`):

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
pythonpath = ["src"]
```

## Common Test Commands

```bash
# Quick test run
pytest

# Full test suite with coverage
pytest --cov=villa_ecommerce_sdk --cov-report=term --cov-report=html

# Run only fast tests (skip integration tests)
pytest -m "not integration"

# Run tests and stop on first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run tests and show coverage for specific module
pytest --cov=villa_ecommerce_sdk.client tests/test_client.py
```

## Troubleshooting

### Import Errors

If you get import errors, ensure you're in the `python/` directory and the package is installed:

```bash
cd python
pip install -e .
```

### Missing Dependencies

Install all dependencies:

```bash
pip install -r requirements.txt
pip install pytest pytest-cov
```

### AWS Credentials for Integration Tests

Some integration tests may require AWS credentials. Set them up:

```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=ap-southeast-1
```

Or configure AWS CLI:

```bash
aws configure
```

## Coverage Reports

After running tests with coverage, view the HTML report:

```bash
# Generate HTML report
pytest --cov=villa_ecommerce_sdk --cov-report=html

# Open in browser (macOS)
open htmlcov/index.html

# Open in browser (Linux)
xdg-open htmlcov/index.html

# Open in browser (Windows)
start htmlcov/index.html
```



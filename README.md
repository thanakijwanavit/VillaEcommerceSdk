# Villa Ecommerce SDK

Multi-language SDKs and API clients for interacting with Villa Ecommerce APIs. This repository provides SDK implementations in Swift, Python, and JavaScript/TypeScript.

## Overview

The Villa Ecommerce SDK provides tools for making authenticated requests to the Villa Ecommerce API with support for multiple authentication methods, caching, and data manipulation.

## Available SDKs

### Swift SDK

A Swift package for iOS and macOS applications.

**Features:**
- Multiple authentication methods (API Key, AWS Cognito, AWS Signature)
- AWS Request Signing with Signature V4
- Type-safe requests with Codable
- Async/Await support (iOS 15+)
- Alamofire integration

**Installation:**
```swift
dependencies: [
    .package(url: "https://github.com/your-org/VillaEcommerceSdk.git", from: "1.0.0")
]
```

**Documentation:** See [Swift SDK README](Sources/VillaEcommerceSdk/README.md) or the main [README](README.md) above.

### Python SDK

A Python package for fetching product lists and inventory data with S3-based caching.

**Features:**
- Product list fetching from Villa Market APIs
- Inventory data retrieval
- S3-based caching for API responses
- Pandas DataFrame support
- Data merging and filtering capabilities

**Installation:**
```bash
pip install villa-ecommerce-sdk
```

**Quick Start:**
```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="villa-ecommerce-sdk-cache")
products_df = client.get_product_list(branch=1000)
inventory_df = client.get_inventory(branch=1000)
merged_df = client.get_products_with_inventory(branch=1000)
```

**Documentation:** See [Python SDK README](python/README.md)

**Infrastructure:** See [AWS Setup Guide](docs/aws-setup/README.md) for deploying the S3 cache bucket.

### JavaScript/TypeScript SDK

Coming soon - JavaScript/TypeScript SDK implementation.

## Repository Structure

```
VillaEcommerceSdk/
├── Sources/                    # Swift SDK source code
│   └── VillaEcommerceSdk/
├── python/                     # Python SDK
│   ├── src/
│   │   └── villa_ecommerce_sdk/
│   ├── tests/
│   ├── template.yaml          # SAM template for S3 bucket
│   └── README.md
├── javascript/                 # JavaScript/TypeScript SDK (coming soon)
├── docs/                       # Documentation
│   └── aws-setup/             # AWS infrastructure setup guides
├── .github/
│   └── workflows/             # CI/CD workflows
└── README.md                   # This file
```

## Features

### Common Features Across SDKs

- **Multiple Authentication Methods**: Support for API Key, AWS Cognito, and AWS Signature authentication
- **AWS Integration**: Built-in AWS services integration
- **Type Safety**: Strong typing and validation
- **Error Handling**: Comprehensive error handling and retry logic

### Python-Specific Features

- **S3 Caching**: Automatic caching of API responses to S3
- **DataFrame Support**: All data returned as pandas DataFrames
- **Data Manipulation**: Built-in merging and filtering capabilities

### Swift-Specific Features

- **Async/Await**: Modern Swift concurrency support
- **Codable Integration**: Type-safe request/response handling
- **Alamofire**: Built on Alamofire for robust networking

## Requirements

### Swift SDK
- iOS 14.0+ / macOS 10.13+
- Swift 5.5+
- Xcode 13.0+

### Python SDK
- Python 3.8 or higher
- AWS credentials configured (for S3 caching)
- An S3 bucket for caching API responses

## Quick Start Examples

### Swift

```swift
import VillaEcommerceSdk

let api = VillaApi()
api.getRequest(
    of: YourResponseType.self,
    authorization: .apiKey(apikey: "your-api-key"),
    url: "https://villa.kitchen/api/endpoint",
    functionName: "getData"
) { result in
    // Handle result
}
```

### Python

```python
from villa_ecommerce_sdk import VillaClient

client = VillaClient(s3_bucket="my-bucket")
products_df = client.get_product_list(branch=1000)
merged_df = client.get_products_with_inventory(
    branch=1000,
    filters={"category": "electronics"}
)
```

## Infrastructure Setup

For Python SDK users, you'll need an S3 bucket for caching. See [AWS Setup Guide](docs/aws-setup/README.md) for:

- Automated setup scripts
- CloudFormation/SAM templates
- GitHub Actions deployment workflows

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. **Swift SDK**: Open in Xcode or use Swift Package Manager
2. **Python SDK**: 
   ```bash
   cd python
   pip install -e .
   pytest tests/
   ```
3. **JavaScript SDK**: Coming soon

## CI/CD

This repository includes GitHub Actions workflows for:
- **Deployment**: Deploy S3 cache bucket infrastructure
- **Publishing**: Publish Python package to PyPI

See `.github/workflows/` for workflow definitions.

## License

MIT License - see [LICENSE](python/LICENSE) file for details.

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

## Links

- [Python SDK Documentation](python/README.md)
- [AWS Infrastructure Setup](docs/aws-setup/README.md)
- [Python SDK PyPI Package](https://pypi.org/project/villa-ecommerce-sdk/)

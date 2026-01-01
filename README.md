# Villa Ecommerce SDK (Swift)

A Swift SDK and API client for obtaining data from Villa Ecommerce. This SDK provides tools for making authenticated requests to the Villa Ecommerce API with support for multiple authentication methods.

> **Note**: SDKs are also available in [Python](#other-language-sdks) and [JavaScript](#other-language-sdks). This repository contains the Swift implementation.

## Overview

The Villa Ecommerce SDK is a Swift package that simplifies interaction with the Villa Ecommerce API. It handles authentication, request signing, and response parsing, making it easy to integrate Villa Ecommerce data into your iOS or macOS applications.

## Features

- **Multiple Authentication Methods**: Support for API Key, AWS Cognito, and AWS Signature authentication
- **AWS Request Signing**: Built-in AWS Signature V4 signing for secure API requests
- **Type-Safe Requests**: Decodable response handling with Swift's Codable protocol
- **Async/Await Support**: Modern Swift concurrency support (iOS 15+)
- **Alamofire Integration**: Built on top of Alamofire for robust networking

## Requirements

- iOS 14.0+ / macOS 10.13+
- Swift 5.5+
- Xcode 13.0+

## Installation

### Swift Package Manager

Add the following to your `Package.swift` file:

```swift
dependencies: [
    .package(url: "https://github.com/your-org/VillaEcommerceSdk.git", from: "1.0.0")
]
```

Or add it through Xcode:
1. File → Add Packages...
2. Enter the repository URL
3. Select the version you want to use

## Usage

### Basic Setup

```swift
import VillaEcommerceSdk

// Initialize with default base URL (https://villa.kitchen/)
let api = VillaApi()

// Or specify a custom base URL
let api = VillaApi(baseUrl: "https://your-custom-url.com/")
```

### Authentication Methods

The SDK supports three authentication methods:

#### 1. No Authentication

```swift
let api = VillaApi()
api.getRequest(
    of: YourResponseType.self,
    authorization: .none,
    url: "https://villa.kitchen/api/endpoint",
    functionName: "getData"
) { result in
    // Handle result
}
```

#### 2. API Key Authentication

```swift
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

#### 3. AWS Cognito Authentication

```swift
let api = VillaApi()
api.getRequest(
    of: YourResponseType.self,
    authorization: .cognito(cognitoKey: "your-cognito-token"),
    url: "https://villa.kitchen/api/endpoint",
    functionName: "getData"
) { result in
    // Handle result
}
```

#### 4. AWS Signature Authentication

```swift
import AWSSigner
import NIOHTTP1

let awsSignature = AwsSignature()
let headers = NIOHTTP1.HTTPHeaders([("Content-Type", "application/json")])

let signedHeaders = awsSignature.getAwsHeader(
    key: "your-access-key",
    secret: "your-secret-key",
    url: "https://villa.kitchen/api/endpoint",
    method: .get,
    headers: headers,
    body: nil
)

// Use signedHeaders with your Alamofire request
```

### API Key Helper

The `ApiKey` class provides convenient methods for retrieving API keys:

#### Using Completion Handler

```swift
let apiKey = ApiKey()
apiKey.getMockupKey(
    path: "auth/check/cognitotest1",
    authorization: .cognito(cognitoKey: "your-token")
) { key in
    if let key = key {
        print("Retrieved API key: \(key)")
    }
}
```

#### Using Async/Await (iOS 15+)

```swift
@available(iOS 15.0, *)
func fetchApiKey() async {
    let apiKey = ApiKey()
    if let key = await apiKey.getMockupKey(
        authorization: .cognito(cognitoKey: "your-token")
    ) {
        print("Retrieved API key: \(key)")
    }
}
```

### Custom Request Types

Define your response models using Swift's `Codable` protocol:

```swift
struct ProductResponse: Codable {
    let id: String
    let name: String
    let price: Double
}

let api = VillaApi()
api.getRequest(
    of: ProductResponse.self,
    authorization: .apiKey(apikey: "your-key"),
    url: "https://villa.kitchen/api/products/123",
    functionName: "getProduct"
) { product in
    if let product = product {
        print("Product: \(product.name)")
    }
}
```

## API Reference

### VillaApi

Main API client class for making requests to Villa Ecommerce.

#### Methods

- `init(baseUrl: String)` - Initialize with a custom base URL (defaults to `https://villa.kitchen/`)
- `getRequest<T: Decodable>(of:authorization:url:functionName:callback:)` - Make a GET request with type-safe response handling

#### Authorization Enum

```swift
enum Authorization {
    case none
    case apiKey(apikey: String)
    case cognito(cognitoKey: String)
    case aws(key: String, secret: String)
}
```

### ApiKey

Helper class for API key management.

#### Methods

- `getMockupKey(path:authorization:callback:)` - Retrieve an API key using completion handler
- `getMockupKey(authorization:) async -> String?` - Retrieve an API key using async/await (iOS 15+)

### AwsSignature

Utility class for AWS Signature V4 signing.

#### Methods

- `getAwsHeader(key:secret:url:method:headers:body:) -> HTTPHeaders` - Generate AWS-signed headers
- `staticGetAwsHeader(key:secret:url:method:headers:body:) -> HTTPHeaders` - Static convenience method

## Dependencies

- [Alamofire](https://github.com/Alamofire/Alamofire) - HTTP networking library
- [aws-signer-v4](https://github.com/adam-fowler/aws-signer-v4) - AWS Signature V4 signing
- [Yams](https://github.com/jpsim/Yams) - YAML parsing library

## Other Language SDKs

This SDK is also available in other languages:
- **Python**: For Python usage, please refer to the Python SDK documentation
- **JavaScript**: For JavaScript/TypeScript usage, please refer to the JavaScript SDK documentation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your license information here]

## Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

// swift-tools-version:5.5
// The swift-tools-version declares the minimum version of Swift required to build this package.

import PackageDescription

let package = Package(
    name: "VillaEcommerceSdk",
    platforms: [
//        .iOS(.v13),
        .iOS(.v14),
    ],
    products: [
        .library(
            name: "VillaEcommerceSdk",
            targets: ["VillaEcommerceSdk"]),
    ],
    dependencies: [
        // Dependencies declare other packages that this package depends on.
        // .package(url: /* package url */, from: "1.0.0"),
        .package(url: "https://github.com/Alamofire/Alamofire", .upToNextMajor(from: "5.4.2") ),
        .package(url: "https://github.com/adam-fowler/aws-signer-v4.git", .upToNextMajor(from: "2.1.1"))
    ],
    targets: [
        // Targets are the basic building blocks of a package. A target can define a module or a test suite.
        // Targets can depend on other targets in this package, and on products in packages this package depends on.
        .target(
            name: "VillaEcommerceSdk",
            dependencies: [
                "Alamofire",
                .product(name: "AWSSigner", package: "aws-signer-v4")
            ]),
        .testTarget(
            name: "VillaEcommerceSdkTests",
            dependencies: ["VillaEcommerceSdk"]),
    ]
)

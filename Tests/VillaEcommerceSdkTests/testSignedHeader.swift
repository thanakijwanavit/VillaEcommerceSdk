//
//  testSignedHeader.swift
//  VillaEcommerceSdkTests
//
//  Created by nic wanavit on 6/27/21.
//

import XCTest
@testable import VillaEcommerceSdk

class testSignedHeader: XCTestCase {


    @available(iOS 15, *)
    func test_signing() throws {
        let result = AwsSignature.staticGetAwsHeader(key: "test", secret: "test", url: "https://test.com", method: .get, headers: ["test":"test"], body: nil)
        
        debugPrint("result is \(result)")
    }

}

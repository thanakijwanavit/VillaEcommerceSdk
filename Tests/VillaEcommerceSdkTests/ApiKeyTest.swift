//
//  File.swift
//  
//
//  Created by nic wanavit on 6/26/21.
//

import Foundation
import XCTest
@testable import VillaEcommerceSdk

final class ApiKeyTest: XCTestCase {
    func testExample() throws {
        XCTAssertEqual(VillaEcommerceSdk().text, "Hello, World!")
    }
    func testGetApiKey(){
        let e = expectation(description: "api key call")
        let apiKey = ApiKey().getMockupKey { result in
            debugPrint(result)
            e.fulfill()
        }
        wait(for: [e], timeout: 5)
    }
    
    @available(macOS 12.0, *)
    @available(iOS 15.0, *)
    func testAwaitGetApiKey(){
        let e = expectation(description: "api key call")
        asyncDetached(priority: .none) {
            let apiKey = await ApiKey().getMockupKey()
            debugPrint("api key from awaitGetApi is:")
            debugPrint(apiKey)
            e.fulfill()
        }
        wait(for: [e], timeout: 5)
    }
    
}

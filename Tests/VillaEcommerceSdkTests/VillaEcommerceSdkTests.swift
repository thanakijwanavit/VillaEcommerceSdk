import XCTest
@testable import VillaEcommerceSdk

final class VillaEcommerceSdkTests: XCTestCase {
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

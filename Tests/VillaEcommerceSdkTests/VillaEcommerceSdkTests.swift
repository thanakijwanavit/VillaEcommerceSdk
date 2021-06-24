import XCTest
@testable import VillaEcommerceSdk

final class VillaEcommerceSdkTests: XCTestCase {
    func testExample() throws {
        XCTAssertEqual(VillaEcommerceSdk().text, "Hello, World!")
    }
    func testGetApiKey(){
        let apiKey = ApiKey.getMockupKey()
    }
}

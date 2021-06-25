//
//  File.swift
//  
//
//  Created by nic wanavit on 6/24/21.
//

import Foundation
import Alamofire

class ApiKey:VillaApi{
    
    
    
    func getMockupKey(path:String = "auth/check/cognitotest1", callback: @escaping (String?)->Void){
        
        class MockupKey:Codable {
            let key:String
        }
        
        let url:String = self.baseUrl + path
        AF.request(url, method: .get)
            .responseDecodable(of: MockupKey.self) { response in
                if let result = response.value{
                    callback(result.key)
                }
            }
            .responseJSON { response in
                debugPrint("error decoding, response is \(String(describing: response.value))")
            }
    }
    
    @available(iOS 15.0, *)
    func getMockupKey()async->String? {
        let result = await withUnsafeContinuation { continuation in
            self.getMockupKey { result in
                continuation.resume(returning: result)
            }
        }
        return result
    }
    
    
    
    
}

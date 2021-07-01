//
//  File.swift
//  
//
//  Created by nic wanavit on 6/24/21.
//

import Foundation
import Alamofire

class ApiKey:VillaApi{
    
    func getMockupKey(path:String = "auth/check/cognitotest1", authorization: VillaApi.Authorization, callback: @escaping (String?)->Void){
        
        class MockupKey:Codable {
            let key:String
        }
        
        let url:String = self.baseUrl + path
        
        self.getRequest(of: MockupKey.self,authorization: authorization, url: url) { mockupKey in
            if let mockupKey = mockupKey{
                callback(mockupKey.key)
            }
        }
        
    }
    
    @available(iOS 15.0, *)
    func getMockupKey( authorization: VillaApi.Authorization )async->String? {
        let result = await withUnsafeContinuation { continuation in
            self.getMockupKey(authorization: authorization) { result in
                continuation.resume(returning: result)
            }
        }
        return result
    }
    
    
    
    
}

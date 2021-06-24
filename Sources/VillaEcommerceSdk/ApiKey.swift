//
//  File.swift
//  
//
//  Created by nic wanavit on 6/24/21.
//

import Foundation
import Alamofire

class ApiKey{
    static func getMockupKey(){
        let url:String = "https://villa.kitchen/auth/check/cognitotest1"
        AF.request(url, method: .get, parameters: nil, headers: nil, interceptor: nil, requestModifier: nil)
    }
}

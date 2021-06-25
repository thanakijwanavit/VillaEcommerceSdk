//
//  File.swift
//  
//
//  Created by nic wanavit on 6/25/21.
//

import Foundation
import Alamofire
import AWSSigner

class VillaApi {
    let baseUrl:String
    
    init( baseUrl:String = "https://villa.kitchen/"){
        self.baseUrl = baseUrl
    }
    
    func getRequest<T:Decodable>(of type: T.Type = T.self, authorization:Authorization = .none, url:String, functionName:String="no function name", callback:@escaping (T?)->Void){
        
        var headers:HTTPHeaders = [:]
        switch authorization {
        case .none:
            debugPrint("\(functionName) uses no authorization")
        case .apiKey(let apikey):
            headers["Authorization"] = apikey
            debugPrint("\(functionName) uses apikey")
        case .cognito(let cognitoKey):
            headers["Authorization"] = cognitoKey
            debugPrint("\(functionName) uses cognitoKey")
        case .aws(let key, let secret):
            debugPrint("\(functionName) uses aws signature")
        }
        
        AF.request(url, method: .get, headers: headers)
            .responseDecodable(of: T.self) { response in
                if let result = response.value{
                    callback(result)
                }
            }
            .responseJSON { response in
                debugPrint("error decoding, response is \(String(describing: response.value))")
            }
    }
    
    
    enum Authorization{
        case none
        case apiKey(apikey:String)
        case cognito(cognitoKey:String)
        case aws(key:String, secret:String)
    }
    
    
    
    func getAwsHeader(key:String, secret:String, url:String, method:HTTPMethod){
        let credentials = StaticCredential(accessKeyId: key, secretAccessKey: secret)
        let signer = AWSSigner(credentials: credentials, name: "s3", region: "us-east-1")
        let signedURL = signer.signURL(
                            url: URL(string:url)!,
                            method: method)
    }
    
}

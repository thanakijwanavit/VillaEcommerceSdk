//
//  File.swift
//  
//
//  Created by nic wanavit on 6/25/21.
//

import Foundation
import Alamofire
import AWSSigner
import NIOHTTP1

class VillaApi {
    let baseUrl:String
    
    init( baseUrl:String = "https://villa.kitchen/"){
        self.baseUrl = baseUrl
    }
    
    func getRequest<T:Decodable>(of type: T.Type = T.self, authorization:Authorization = .none, url:String, functionName:String="no function name", callback:@escaping (T?)->Void){
        
        var headers: Alamofire.HTTPHeaders = [:]
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
    
    
    
//    @available(iOS 15, *)
//    func getAwsHeader(key:String, secret:String, url:String, method: Alamofire.HTTPMethod, headers: NIOHTTP1.HTTPHeaders, body:String? = nil)->Alamofire.HTTPHeaders{
//        let credentials = StaticCredential(accessKeyId: key, secretAccessKey: secret)
//        let signer = AWSSigner(credentials: credentials, name: "s3", region: "us-east-1")
//        let signedHeader = signer.signHeaders(url: URL(string: url)!, method: mapAlamofireToNio(method: method), headers: headers, body: (body != nil) ? .string(body!): nil, date: Date.now)
//        
//        debugPrint(signedHeader)
//        return self.nioToAlamofireHeader(nioHeaders: signedHeader)
//        
//    }
//    
//    func mapAlamofireToNio(method:Alamofire.HTTPMethod)->NIOHTTP1.HTTPMethod{
//        switch method {
//        case .get:
//            print("get")
//            return .GET
//        case .post:
//            print("post")
//            return .POST
//        default:
//            print("default (get)")
//            return .GET
//        }
//    }
//    func nioToAlamofireHeader(nioHeaders:NIOHTTP1.HTTPHeaders)->Alamofire.HTTPHeaders{
//        var headerString:[String:String] = nioHeaders.reduce(into: [String:String]()) {
//            $0[$1.name] = $1.value
//        }
//        return Alamofire.HTTPHeaders(headerString)
//    }
    
}



//extension NIOHTTP1.HTTPHeaders{
//    func alamofireHeaders()->Alamofire.HTTPHeaders{
//        let headerDict:[String:String] = self.headers.reduce(into: [:]) { $0[$1.0] = $1.1 }
//        return Alamofire.HTTPHeaders(headerDict)
//    }
//}
///Users/nic/ios/VillaEcommerceSdk/Sources/VillaEcommerceSdk/VillaApi.swift:61:37: Cannot convert value of type 'Alamofire.HTTPMethod' to expected argument type 'NIOHTTP1.HTTPMethod'

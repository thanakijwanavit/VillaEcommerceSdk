//
//  File.swift
//  
//
//  Created by nic wanavit on 6/29/21.
//

import Foundation
import AWSSigner
import NIOHTTP1
import Alamofire

class AwsSignature{
    @available(iOS 15, *)
    func getAwsHeader(key:String, secret:String, url:String, method: Alamofire.HTTPMethod, headers: NIOHTTP1.HTTPHeaders, body:String? = nil)->Alamofire.HTTPHeaders{
        let credentials = StaticCredential(accessKeyId: key, secretAccessKey: secret)
        let signer = AWSSigner(credentials: credentials, name: "s3", region: "us-east-1")
        let signedHeader = signer.signHeaders(url: URL(string: url)!, method: mapAlamofireToNio(method: method), headers: headers, body: (body != nil) ? .string(body!): nil, date: Date.now)
        
        debugPrint(signedHeader)
        return self.nioToAlamofireHeader(nioHeaders: signedHeader)
        
    }
    
    func mapAlamofireToNio(method:Alamofire.HTTPMethod)->NIOHTTP1.HTTPMethod{
        switch method {
        case .get:
            print("get")
            return .GET
        case .post:
            print("post")
            return .POST
        default:
            print("default (get)")
            return .GET
        }
    }
    func nioToAlamofireHeader(nioHeaders:NIOHTTP1.HTTPHeaders)->Alamofire.HTTPHeaders{
        let headerString:[String:String] = nioHeaders.reduce(into: [String:String]()) {
            $0[$1.name] = $1.value
        }
        return Alamofire.HTTPHeaders(headerString)
    }
    
    @available(iOS 15, *)
    static func staticGetAwsHeader(key:String, secret:String, url:String, method: Alamofire.HTTPMethod, headers: NIOHTTP1.HTTPHeaders, body:String? = nil)->Alamofire.HTTPHeaders{
        let signer = AwsSignature()
        return signer.getAwsHeader(key: key, secret: secret, url: url, method: method, headers: headers, body: body)
        
    }
}

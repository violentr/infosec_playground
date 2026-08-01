package com.violentr.burp.http;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.http.message.HttpRequestResponse;
import burp.api.montoya.http.message.requests.HttpRequest;

public class HandleHttpRequest {
    private MontoyaApi montoyaApi;

    public HandleHttpRequest(MontoyaApi api){
        this.montoyaApi = api;
    }


    public HttpRequestResponse httpRequestFromString(String url){
        HttpRequest req = HttpRequest.httpRequestFromUrl(url);
        return  montoyaApi.http().sendRequest(req);
     }
}

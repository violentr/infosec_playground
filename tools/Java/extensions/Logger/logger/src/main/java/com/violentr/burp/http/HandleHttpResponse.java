package com.violentr.burp.http;

import burp.api.montoya.http.message.HttpHeader;
import burp.api.montoya.http.message.HttpRequestResponse;

import java.util.Optional;

public class HandleHttpResponse {
    private final HttpRequestResponse response;

    public HandleHttpResponse(HttpRequestResponse response){
        this.response = response;
    }

    public String getRequestHeader(String headerName) {
        if (response == null || response.request() == null){
            return "N/A";
        }
        return  Optional.of(response.request()
                .header(headerName))
                .map(HttpHeader::value)
                .orElse("N/A");
    }
    private boolean isResponseNull(){
        return response == null || response.response() == null;
    }

    public String getResponseHeader(String headerName) {
        if (isResponseNull()){
            return "N/A";
        }
        return  Optional.of(response.response()
                .header(headerName))
                .map(HttpHeader::value)
                .orElse("N/A");
    }

    public String getBody(){
        if (isResponseNull()){
            return "N/A";
        }
        return Optional.of(response.response()
                .body())
                .map(Object::toString)
                .orElse("N/A");
    }

    public String getStatus(){
        if (isResponseNull()){
            return "N/A";
        }
        return Optional.of(response.response().statusCode())
                .map(Object::toString)
                .orElse("N/A");
    }

}

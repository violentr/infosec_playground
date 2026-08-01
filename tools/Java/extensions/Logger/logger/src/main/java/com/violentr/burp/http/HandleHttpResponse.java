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
        return  Optional.ofNullable(response.request().header(headerName)).map(HttpHeader::value).orElse("N/A");
    }

    public String getResponseHeader(String headerName) {
        return  Optional.ofNullable(response.response().header(headerName)).map(HttpHeader::value).orElse("N/A");
    }

    public String getBody(){
        return Optional.ofNullable(response.response().body()).map(Object::toString).orElse("N/A");
    }

    public String getStatus(){
        if (response == null || response.response() == null){
            return "N/A";
        }
        return Optional.of(response.response().statusCode())
                .map(Object::toString)
                .orElse("N/A");
    }

}

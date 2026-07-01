package com.violentr.burp;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.http.message.HttpHeader;
import burp.api.montoya.http.message.HttpRequestResponse;
import burp.api.montoya.http.message.requests.HttpRequest;
import burp.api.montoya.http.message.responses.HttpResponse;
import burp.api.montoya.logging.Logging;

import java.util.Optional;

public class BurpExtensionEntry implements BurpExtension {
    private static final String NAME = "Burp extension";
    private MontoyaApi montoyaApi;

    @Override
    public void initialize(MontoyaApi montoyaApi) {
        this.montoyaApi = montoyaApi;
        Logging log = montoyaApi.logging();
        extensionLoad();
        HttpRequest request = HttpRequest.httpRequestFromUrl("https://example.com");
        HttpRequestResponse response = montoyaApi.http().sendRequest(request);
        loggedHeaders(response, log);
    }
    public void extensionLoad(){
        montoyaApi.extension().setName(NAME);
        montoyaApi.logging().logToOutput("extension loaded: " + NAME);
    }
    public void loggedHeaders(HttpRequestResponse response, Logging log){
        log.logToOutput("Burp version " + montoyaApi.burpSuite().version());
            HttpHeader userAgent = response.request().header("User-Agent");
        HttpHeader server = response.response().header("Server");
        log.logToOutput("status code: " + response.response().statusCode());
        log.logToOutput("user agent: " + Optional.ofNullable(userAgent).map(HttpHeader::value).orElse("Not found"));
        log.logToOutput("server: " + Optional.ofNullable(server).map(HttpHeader::value).orElse("Not found"));
        log.logToOutput("response body: " + response.response().body());
    }
}

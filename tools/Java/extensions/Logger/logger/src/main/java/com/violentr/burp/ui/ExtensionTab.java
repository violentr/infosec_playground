package com.violentr.burp.ui;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.core.Registration;
import burp.api.montoya.http.message.HttpHeader;
import burp.api.montoya.http.message.HttpRequestResponse;
import burp.api.montoya.http.message.requests.HttpRequest;
import burp.api.montoya.logging.Logging;
import burp.api.montoya.ui.UserInterface;
import com.violentr.burp.Constants;

import javax.swing.*;
import java.awt.*;
import java.util.Optional;

public class ExtensionTab {
    private final MontoyaApi montoyaApi;

    public ExtensionTab(MontoyaApi api){
        this.montoyaApi = api;
    }
    public void createAndRegisterTab(UserInterface ui) {
        JPanel panel = new JPanel(new BorderLayout(6, 6));
        String url = "https://example.com";
        JTextArea output = new JTextArea();
        output.setEditable(false);
        output.setLineWrap(true);
        output.setWrapStyleWord(true);

        JScrollPane scroll = new JScrollPane(output);
        panel.add(scroll, BorderLayout.CENTER);
        JPanel controls = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JButton sendBtn = new JButton("Send request");
        controls.add(sendBtn);
        panel.add(controls, BorderLayout.NORTH);
        Logging log = montoyaApi.logging();
        // Button action: run HTTP request off the EDT
        sendBtn.addActionListener(e -> {
            sendBtn.setEnabled(false);
            output.append("Starting request to " + url + "...\n");
            // run network I/O off-EDT
            new Thread(() -> {
                try {
                    HttpRequest req = HttpRequest.httpRequestFromUrl(url);
                    HttpRequestResponse response = montoyaApi.http().sendRequest(req);

                    String status = String.valueOf(response.response().statusCode());
                    String body = response.response().body().toString();
                    String userAgent = Optional.ofNullable(response.request().header("User-Agent")).map(HttpHeader::value).orElse("N/A");
                    String server = Optional.ofNullable(response.response().header("Server")).map(HttpHeader::value).orElse("N/A");

                    // update UI on EDT
                    SwingUtilities.invokeLater(() -> {
                        output.append("status: " + status + "\n");
                        output.append("user-agent: " + userAgent + "\n");
                        output.append("server: " + server + "\n");
                        output.append("body snippet: " + (body.length() > 300 ? body.substring(0, 300) + "..." : body) + "\n\n");
                        sendBtn.setEnabled(true);
                    });

                    // also log to Burp Output tab
                    log.logToOutput("request done: status=" + status);
                } catch (Exception ex) {
                    SwingUtilities.invokeLater(() -> {
                        output.append("Request failed: " + ex.getMessage() + "\n");
                        sendBtn.setEnabled(true);
                    });
                    log.logToOutput("request failed: " + ex.getMessage());
                }
            }).start();
        });

        // Register the tab with Burp
        Registration tabRegistration = ui.registerSuiteTab(Constants.NAME, panel);
        // Optionally apply theme via montoyaApi.userInterface().applyThemeToComponent(panel);
    }
}

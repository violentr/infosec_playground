package com.violentr.burp;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.core.Registration;
import burp.api.montoya.http.message.HttpHeader;
import burp.api.montoya.http.message.HttpRequestResponse;
import burp.api.montoya.http.message.requests.HttpRequest;
import burp.api.montoya.logging.Logging;
import burp.api.montoya.ui.UserInterface;

import javax.swing.*;
import java.awt.*;
import java.util.Optional;

public class BurpExtensionEntry implements BurpExtension {
    private static final String NAME = "Burp extension";
    private MontoyaApi montoyaApi;
    private Registration tabRegistration; // keep to deregister later if needed

    @Override
    public void initialize(MontoyaApi montoyaApi) {
        this.montoyaApi = montoyaApi;
        Logging log = montoyaApi.logging();
        log.logToOutput("Burp version " + montoyaApi.burpSuite().version());
        extensionLoad();
        SwingUtilities.invokeLater(() -> createAndRegisterTab(montoyaApi.userInterface(), log));
    }

    public void extensionLoad() {
        montoyaApi.extension().setName(NAME);
        montoyaApi.logging().logToOutput("extension loaded: " + NAME);
    }

    private void createAndRegisterTab(UserInterface ui, Logging log) {
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
                    montoyaApi.logging().logToOutput("request done: status=" + status);
                } catch (Exception ex) {
                    SwingUtilities.invokeLater(() -> {
                        output.append("Request failed: " + ex.getMessage() + "\n");
                        sendBtn.setEnabled(true);
                    });
                    montoyaApi.logging().logToOutput("request failed: " + ex.getMessage());
                }
            }).start();
        });

        // Register the tab with Burp
        tabRegistration = ui.registerSuiteTab(NAME, panel);
        // Optionally apply theme via montoyaApi.userInterface().applyThemeToComponent(panel);
    }
}

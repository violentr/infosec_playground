package com.violentr.burp.ui;

import burp.api.montoya.MontoyaApi;
import burp.api.montoya.core.Registration;
import burp.api.montoya.http.message.HttpHeader;
import burp.api.montoya.http.message.HttpRequestResponse;
import burp.api.montoya.logging.Logging;
import burp.api.montoya.ui.UserInterface;
import com.violentr.burp.Constants;
import com.violentr.burp.http.HandleHttpRequest;
import com.violentr.burp.http.HandleHttpResponse;

import javax.swing.*;
import java.awt.*;
import java.util.Optional;

public class ExtensionTab {
    private final MontoyaApi montoyaApi;
    private JPanel panel;
    public ExtensionTab(MontoyaApi api){
        this.montoyaApi = api;
    }

    private void createTab(UserInterface ui){
        panel = new JPanel(new BorderLayout(6, 6));
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
                    HttpRequestResponse response = new HandleHttpRequest(montoyaApi).httpRequestFromString(url);
                    HandleHttpResponse handleResponse = new HandleHttpResponse(response);

                    String status = handleResponse.getStatus();
                    String body = handleResponse.getBody();
                    String userAgent = handleResponse.getRequestHeader("User-Agent");
                    String server = handleResponse.getResponseHeader("Server");

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
    }
    private void registerTab(UserInterface ui, JPanel panel){
        ui.registerSuiteTab(Constants.NAME, panel);
    }
    public void createAndRegisterTab(UserInterface ui) {
        createTab(ui);
        registerTab(ui, panel);
    }
}

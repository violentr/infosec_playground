package com.violentr.burp;

import burp.api.montoya.BurpExtension;
import burp.api.montoya.MontoyaApi;
import burp.api.montoya.logging.Logging;
import com.violentr.burp.ui.ExtensionTab;

import javax.swing.*;

public class BurpExtensionEntry implements BurpExtension {
    private MontoyaApi montoyaApi;

    @Override
    public void initialize(MontoyaApi montoyaApi) {
        this.montoyaApi = montoyaApi;
        montoyaApi.extension().setName(Constants.NAME);
        ExtensionTab extensionTab = new ExtensionTab(montoyaApi);
        initialLogging();
        SwingUtilities.invokeLater(() -> extensionTab.createAndRegisterTab(montoyaApi.userInterface()));
    }
    private void initialLogging(){
        Logging log =  montoyaApi.logging();
        log.logToOutput("Burp version " + montoyaApi.burpSuite().version());
        log.logToOutput("extension loaded: " + Constants.NAME);
    }
}

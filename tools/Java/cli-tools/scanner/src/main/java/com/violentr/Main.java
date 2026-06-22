package src.main.java.com.violentr;

import java.io.IOException;

public class Main {
    private static void validateHostname(String hostname) {
        if (hostname == null || hostname.isBlank()) {
            throw new IllegalArgumentException("Hostname required");
        }
        // allow letters, digits, dots, hyphens only
        if (!hostname.matches("[a-zA-Z0-9.-]+")) {
            throw new IllegalArgumentException("Invalid hostname: " + hostname);
        }
    }

    public static void main(String[] args) {
        if (args.length != 2) {
            System.out.println("Usage: scanner <tool> <hostname>");
            System.out.println("Tools: nmap, sqlmap, ...");
            return;
        }
        String toolName = args[0];
        String hostname = args[1];

        try{
            validateHostname(hostname);
            System.out.println("PATH: " + System.getProperty("user.dir"));
            ScanTool scanTool = new ScanTool("tools.json");
            scanTool.executeTool(toolName, hostname);
        }catch (IllegalArgumentException e) {
            System.out.println(e.getMessage());
            return;
        }catch (Exception e) {
            System.out.println("Error loading configuration: " + e.getMessage());
        }
    }
}

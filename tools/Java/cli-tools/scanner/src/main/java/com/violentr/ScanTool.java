package src.main.java.com.violentr;

import org.json.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

class ScanTool {
    private final Map<String, String> toolConfigs;

    public ScanTool(String configPath) throws IOException {
        this.toolConfigs = new HashMap<>();
        loadConfig(configPath);
    }

    private void loadConfig(String configPath) throws IOException {
        String content = new String(Files.readAllBytes(Paths.get(configPath)));
        JSONObject json = new JSONObject(content);
        JSONObject tools = json.getJSONObject("tools");

        for (String key : tools.keySet()) {
            toolConfigs.put(key, tools.getString(key));
        }
    }

    public void executeTool(String toolName, String hostname) {
        if (!toolConfigs.containsKey(toolName)) {
            System.out.println("Error: Tool '" + toolName + "' not found in configuration");
            return;
        }

        String command = toolConfigs.get(toolName).replace("{hostname}", hostname);
        String[] commandTool = command.split("\\s+");
        System.out.println("Executing: " + command);
        executeCommand(commandTool);
    }

    private void executeCommand(String[] cmd) {
        try {
            ProcessBuilder pb = new ProcessBuilder(cmd);
            pb.redirectErrorStream(true);
            Process process = pb.start();
            java.io.BufferedReader reader = new java.io.BufferedReader(
                    new java.io.InputStreamReader(process.getInputStream())
            );
            String line;
            while ((line = reader.readLine()) != null) {
                System.out.println(line);
            }
            int exitCode = process.waitFor();
            System.out.println("Exit code: " + exitCode);
        } catch (IOException | InterruptedException e) {
            System.out.println("Error executing command: " + e.getMessage());
        }
    }

    public void showHelp() {
        System.out.println("Available tools:");
        toolConfigs.keySet().forEach(tool -> System.out.println("  - " + tool));
    }
}
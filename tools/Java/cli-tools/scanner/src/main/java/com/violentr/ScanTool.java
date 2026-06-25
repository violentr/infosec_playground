package src.main.java.com.violentr;

import java.io.IOException;
import java.util.Map;

class ScanTool {
    private final Map<String, Tool> toolConfigs;
    private final CommandRunner runner = new CommandRunner();

    public ScanTool(String configPath) throws IOException {
        this.toolConfigs = new ConfigLoader(configPath).load();
    }

    public void executeTool(String toolName, Host host) {
        if (!toolConfigs.containsKey(toolName)) {
            System.out.println("Error: Tool '" + toolName + "' not found in configuration");
            return;
        }
        Tool tool  = toolConfigs.get(toolName);
        String[] resolved = tool.buildCommand(host);
        System.out.println("Executing: " + String.join(" ", resolved));
        runner.run(resolved);
    }

    public void showHelp() {
        System.out.println("Available tools:");
        toolConfigs.keySet().forEach(tool -> System.out.println("  - " + tool));
    }
}

package src.main.java.com.violentr;

import java.io.IOException;
import java.util.Map;

class ScanTool {
    private final ToolRegistry registry;
    private final CommandRunner runner = new CommandRunner();

    public ScanTool(String configPath) throws IOException {
        Map<String, Tool> loaded = new ConfigLoader(configPath).load();
        this.registry = new ToolRegistry(loaded);
    }

    public void executeTool(String toolName, Host host) {
        if (!registry.has(toolName)) {
            System.out.println("Error: Tool '" + toolName + "' not found in configuration");
            return;
        }
        Tool tool  = registry.get(toolName);
        Command resolved = tool.buildCommand(host);
        System.out.println("Executing: " + resolved);
        runner.run(resolved);
    }

    public void showHelp() {
        System.out.println("Available tools:");
        registry.listNames().forEach(tool -> System.out.println("  - " + tool));
    }
}

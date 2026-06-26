package src.main.java.com.violentr;

import java.util.Map;
import java.util.Set;

public class ToolRegistry {
    private final Map<String, Tool> tools;

    public ToolRegistry(Map<String, Tool> tools) {
        this.tools = tools;
    }

    public Tool get(String name) {
        return tools.get(name);
    }
    public boolean has(String name){
        return tools.containsKey(name);
    }
    public Set<String> listNames() {
        return tools.keySet();
    }
}

package src.main.java.com.violentr;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.Map;

public class ConfigLoader {
    final String configPath;

    public ConfigLoader(String configPath)  {
        this.configPath = configPath;
    }
    public Map<String, Tool> load() throws IOException {
        Map<String, Tool> toolConfigs = new HashMap<>();
        String content = new String(Files.readAllBytes(Paths.get(configPath)));
        JSONObject json = new JSONObject(content);
        JSONObject tools = json.getJSONObject("tools");


        for (String key : tools.keySet()) {
            JSONArray args = tools.getJSONArray(key);
            String[] command = new String[args.length()];
            for (int i = 0; i < args.length(); i++) {
                command[i] = args.getString(i);
            }
            Tool tool = new Tool(key, command);
            toolConfigs.put(key, tool);
        }
        return toolConfigs;
    }
}

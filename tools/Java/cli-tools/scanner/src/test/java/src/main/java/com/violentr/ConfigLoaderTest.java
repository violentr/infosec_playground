package src.main.java.com.violentr;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.io.TempDir;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ConfigLoaderTest {

    @Test
    void loadParsesToolDefinitions(@TempDir Path tempDir) throws Exception {
        Path configFile = tempDir.resolve("tools.json");
        String json = """
                {
                  "tools": {
                    "nmap": ["nmap", "-sV", "{hostname}"],
                    "ffuf": ["ffuf", "-u", "http://{hostname}/FUZZ"]
                  }
                }
                """;
        Files.writeString(configFile, json);

        Map<String, Tool> tools = new ConfigLoader(configFile.toString()).load();

        assertTrue(tools.containsKey("nmap"));
        assertTrue(tools.containsKey("ffuf"));
        assertArrayEquals(
                new String[]{"nmap", "-sV", "example.com"},
                tools.get("nmap").buildCommand(new Host("example.com")).toArray()
        );
    }
}


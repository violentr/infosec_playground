package src.main.java.com.violentr;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;

class ToolTest {

    @Test
    void buildCommandReplacesHostnamePlaceholders() {
        Tool tool = new Tool("scanner", new String[]{"nmap", "-sV", "{hostname}", "https://{hostname}/"});
        Host host = new Host("example.com");

        Command resolved = tool.buildCommand(host);

        assertArrayEquals(
                new String[]{"nmap", "-sV", "example.com", "https://example.com/"},
                resolved.toArray()
        );
    }
}


package src.main.java.com.violentr;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class HostTest {

    @Test
    void acceptsValidHostname() {
        Host host = new Host("example.com");
        assertEquals("example.com", host.getValue());
    }

    @Test
    void rejectsBlankHostname() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class, () -> new Host("   "));
        assertEquals("Hostname required", ex.getMessage());
    }

    @Test
    void rejectsInvalidCharacters() {
        assertThrows(IllegalArgumentException.class, () -> new Host("example.com;rm"));
    }
}


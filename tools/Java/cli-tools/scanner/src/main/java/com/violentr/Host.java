package src.main.java.com.violentr;

public class Host {
    private final String value;
    public Host(String hostname) {
        if (hostname == null || hostname.isBlank()) {
            throw new IllegalArgumentException("Hostname required");
        }
        // allow letters, digits, dots, hyphens only
        if (!hostname.matches("[a-zA-Z0-9.-]+")) {
            throw new IllegalArgumentException("Invalid hostname: " + hostname);
        }
        this.value = hostname;
    }
    public String getValue() {
        return value;
    }
}

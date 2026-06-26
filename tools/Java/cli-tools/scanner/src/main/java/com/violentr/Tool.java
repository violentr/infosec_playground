package src.main.java.com.violentr;

public class Tool {
    private final String name;
    private final String[] args;

    public Tool(String name, String[] args) {
        this.name = name;
        this.args = args;
    }
    public Command buildCommand(Host host) {
     String[] resolved = new String[args.length];
     for (int i = 0; i < args.length; i++) {
         resolved[i] = args[i].replace("{hostname}", host.getValue() );
     }
     return new Command(resolved);
    }

    public String getName() {
        return name;
    }
}

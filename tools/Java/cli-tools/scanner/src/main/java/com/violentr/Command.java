package src.main.java.com.violentr;

public class Command {
    private final String[] args;

    public Command(String[] args) {
        this.args = args;
    }

    public String[] toArray() {
        return args;
    }

    @Override
    public String toString() {
        return String.join(" ", args);
    }
}


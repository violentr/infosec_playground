# Scanner CLI Tool

A lightweight Java command-line wrapper for running security scanning tools against a target hostname. Tool commands are defined in `tools.json`, so you can add or change scanners without recompiling.

## Usage

```bash
scanner <tool> <hostname>
```

| Argument   | Description                                      |
|------------|--------------------------------------------------|
| `tool`     | Scanner name from `tools.json` (e.g. `nmap`)     |
| `hostname` | Target host or domain (letters, digits, `.`, `-`) |

### Examples

```bash
scanner nmap example.com
scanner sqlmap test.example.org
```

## Configuration

Commands live in `tools.json`. Use `{hostname}` as a placeholder for the target:

```json
{
  "tools": {
    "nmap": "nmap -sV -A -p 80,443 {hostname}",
    "sqlmap": "sqlmap -u https://{hostname}/ --batch --level 3"
  }
}
```

Run the CLI from the directory that contains `tools.json`, or place a copy of the file in your working directory.

## Build & Run

Requires Java 21 and Maven. Run from the directory that contains `tools.json`. External tools (`nmap`, `sqlmap`, etc.) must be on your `PATH`.

**Recommended — fat JAR:**

```bash
mvn package
java -jar target/scanner-cli-tool-1.0-SNAPSHOT.jar nmap example.com
```

**Quick local run:**

```bash
mvn exec:java -Dexec.mainClass="src.main.java.com.violentr.Main" -Dexec.args="nmap scanme.nmap.org"
```

**Manual run (optional)** — only if you want to run compiled classes without packaging. Compiles to `out/` and copies dependencies to `target/dependency/` so `org.json` is on the classpath:

```bash
mvn clean compile dependency:copy-dependencies
java -cp "out:target/dependency/*" src.main.java.com.violentr.Main nmap scanme.nmap.org
```

On Windows, use `;` instead of `:` in the classpath.

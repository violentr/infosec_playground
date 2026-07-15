# Burp Logger Extension

A learning-focused Burp Suite extension built with the Montoya API that enables detailed logging of HTTP request/response data directly from the Burp proxy context menu.

## Features

- **User-triggered logging**: Right-click on any request/response in Proxy, Repeater, or other tools to log details
- **Safe initialization**: No network calls during extension startup (non-blocking load)
- **Header inspection**: Automatically extracts and logs User-Agent, Server, and other HTTP headers
- **Safe body handling**: Preview-mode response bodies with truncation to avoid output spam
- **Clean logging**: Status codes, response lengths, and request URLs logged to Burp output

## Project Structure

```
logger/
├── src/main/java/com/violentr/burp/
│   └── BurpExtensionEntry.java          # Main extension class
├── pom.xml                               # Maven configuration
└── target/
    └── burp-logger.jar                   # Built extension (after mvn package)
```

## Prerequisites

- **Java 21** or later
- **Maven 3.6+**
- **Burp Suite Community or Professional** (2024.8+)

## Quick Start

### 1. Clean and Build

```bash
cd /$HOME/infosec_playground/tools/Java/extensions/Logger/logger
mvn clean
mvn package
```

After successful build, the packaged extension will be:
```
target/burp-logger.jar
```

### 2. Load into Burp Suite

1. Open Burp Suite
2. Go to **Extensions** → **Installed** (or **Add** if first time)
3. Click **Add** and select the JAR file:
   ```
   target/burp-logger.jar
   ```
4. The extension loads with message: `"Loaded: Burp Logger (Learning)"`


## Maven Commands Reference

| Command | Purpose |
|---------|---------|
| `mvn clean` | Delete `target/` directory and build artifacts |
| `mvn compile` | Compile Java source files only (no JAR) |
| `mvn package` | Compile, run tests, and create JAR in `target/` |
| `mvn clean package` | Full clean build (recommended) |
| `mvn test` | Run unit tests (if added later) |
| `mvn install` | Install JAR to local Maven repository |
| `mvn clean package -DskipTests` | Build without running tests |

## Typical Workflow

```bash
# Full clean rebuild
mvn clean package

# Quick rebuild after code changes
mvn package

# If you want verbose build output
mvn clean package -X

# Skip tests for faster builds (as project grows)
mvn clean package -DskipTests
```

## Project Configuration

- **Java version**: 21
- **Source encoding**: UTF-8
- **Burp Montoya API**: 2026.4
- **Main entry point**: `com.violentr.burp.BurpExtensionEntry`
- **Additional dependency**: Google Gson 2.10.1 (for future JSON processing)

## Troubleshooting

**Extension won't load in Burp:**
- Ensure Java 21+ is installed: `java -version`
- Check Burp logs for errors
- Rebuild with: `mvn clean package`

**Compilation errors:**
- Verify Maven sees Java 21: `mvn -v`
- Clear Maven cache: `rm -rf ~/.m2/repository && mvn clean compile`

**No context menu option appears:**
- Reload/restart Burp Suite after loading extension
- Check Burp's logging output tab for load confirmation


## Resources

- [Burp Suite Montoya API Docs](https://portswigger.net/burp/documentation/desktop/extensions/montoya)
- [Building Burp Extensions](https://portswigger.net/burp/documentation/desktop/extensions/guide)
- [Maven Official Guide](https://maven.apache.org/guides/)

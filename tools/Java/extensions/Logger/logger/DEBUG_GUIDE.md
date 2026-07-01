# Debugging Guide: Exploring Undocumented APIs

This guide documents the process for exploring and understanding Java APIs when documentation is sparse or unclear.

---

## Overview

When you encounter an API with poor documentation, you can:
1. Find the JAR file
2. Search for the class
3. Extract the class from JAR
4. Decompile to see method signatures
5. Filter and search for specific methods

---

## Step-by-Step Process

### 1️⃣ **Identify the Dependency Version**

Check your `pom.xml` to find the exact version:

```xml
<dependency>
    <groupId>net.portswigger.burp.extensions</groupId>
    <artifactId>montoya-api</artifactId>
    <version>2026.4</version>  <!-- ← Version you need -->
</dependency>
```

---

### 2️⃣ **Locate the JAR in Maven Cache**

Maven downloads JARs to `~/.m2/repository`. Find your specific JAR:

```bash
find ~/.m2/repository -name "*montoya*" -type f
```

Output example:
```
/$HOME/.m2/repository/net/portswigger/burp/extensions/montoya-api/2026.4/montoya-api-2026.4.jar
```

**Save this path for reuse!**

---

### 3️⃣ **List All Classes in JAR**

Use `jar -tf` to list contents:

```bash
jar -tf ~/.m2/repository/net/portswigger/burp/extensions/montoya-api/2026.4/montoya-api-2026.4.jar | grep -i "HttpRequest"
```

This searches for classes matching a pattern. Useful to:
- Find the exact class name
- See all related classes
- Navigate the package structure

---

### 4️⃣ **Extract the Class File**

Use `jar -xf` to extract a specific class:

```bash
# Extract single class
jar -xf ~/.m2/repository/net/portswigger/burp/extensions/montoya-api/2026.4/montoya-api-2026.4.jar \
  burp/api/montoya/http/message/HttpRequestResponse.class

# Run from /tmp to keep workspace clean
cd /tmp && jar -xf ~/.m2/repository/.../montoya-api-2026.4.jar burp/api/montoya/...
```

**Why /tmp?** Keeps your working directory clean; extraction creates directory structure.

---

### 5️⃣ **Decompile the Class**

Use `javap` to view method signatures:

```bash
# Basic decompile (method signatures only)
javap burp/api/montoya/http/message/HttpRequestResponse.class

# Verbose mode (includes implementation details)
javap -v burp/api/montoya/http/message/HttpRequestResponse.class

# Show only public methods
javap -public burp/api/montoya/http/message/HttpRequestResponse.class
```

---

### 6️⃣ **Search for Specific Methods**

Combine `javap` with `grep` to find what you need:

```bash
# Find all static methods
javap -v HttpRequestResponse.class | grep "public static"

# Find specific method
javap -v HttpRequestResponse.class | grep -i "sendRequest"

# Find method with context (lines before/after)
javap -v HttpRequestResponse.class | grep -i -C 3 "sendRequest"
```

---

## Complete One-Liner Example

**Goal:** Find all public static factory methods in HttpRequest class

```bash
cd /tmp && \
jar -xf ~/.m2/repository/net/portswigger/burp/extensions/montoya-api/2026.4/montoya-api-2026.4.jar \
  burp/api/montoya/http/message/requests/HttpRequest.class && \
javap -v burp/api/montoya/http/message/requests/HttpRequest.class | grep -A 5 "public static"
```

**Breakdown:**
- `cd /tmp` - work in temp directory
- `jar -xf ... .jar path/to/Class.class` - extract class from JAR
- `javap -v Class.class` - decompile with verbose output
- `grep -A 5 "public static"` - find static methods with 5 lines of context

---

## Common Patterns to Search For

### Find All Methods
```bash
javap -public ClassName.class | grep "public "
```

### Find Static Methods Only
```bash
javap -v ClassName.class | grep "public static"
```

### Find Method Parameters
```bash
javap -v ClassName.class | grep -A 2 "descriptor:"
```

### Find Interfaces Implemented
```bash
javap -v ClassName.class | grep "implements"
```

### Find All Abstract Methods (Interface)
```bash
javap ClassName.class | grep "public abstract"
```

---

## Tips & Tricks

✅ **Always use `/tmp` for extraction** - keeps your project clean
```bash
cd /tmp && jar -xf /path/to/library.jar ...
```

✅ **Use grep with context flags** - see more info
```bash
-B 3  # Show 3 lines BEFORE match
-A 3  # Show 3 lines AFTER match
-C 3  # Show 3 lines BEFORE and AFTER
```

✅ **Escape special characters in grep** - Java types use `<>` and `$`
```bash
# Search for generics (angle brackets)
grep "List<String>" FileName  # Works fine in grep

# Search for inner classes (dollar signs)
grep "Class\$Inner" FileName  # Escape the $ with \
```

✅ **Check if class is interface or concrete**
```bash
javap ClassName.class | head -1
# Output: "public interface ..." → it's an interface
# Output: "public class ..." → it's a concrete class
```

---

## Common Issues & Solutions

### ❌ "Cannot find file"
```bash
# Wrong: javap doesn't work with JAR paths
javap library.jar com.example.ClassName

# Correct: Extract first, then decompile
jar -xf library.jar path/to/ClassName.class
javap path/to/ClassName.class
```

### ❌ "javap: class not found"
```bash
# Wrong: Extracted but not in classpath
cd /home/user && javap burp/api/montoya/Http.class

# Correct: Run from where class file was extracted or use full path
javap /full/path/to/Http.class
```

### ❌ Grep returns nothing
```bash
# Try case-insensitive search
grep -i "methodname" 

# Check if class file is valid
javap ClassName.class  # See if it decompiles at all
```

---

## Real Example: Finding HttpRequest Factory Methods

**Problem:** How do I create an HttpRequest? The docs don't say.

**Solution:**

```bash
# Step 1: Find the JAR
find ~/.m2/repository -name "*montoya*" -type f
# Result: ~/.m2/repository/.../montoya-api-2026.4.jar

# Step 2: List HttpRequest classes
jar -tf ~/.m2/repository/.../montoya-api-2026.4.jar | grep "HttpRequest"
# Result: burp/api/montoya/http/message/requests/HttpRequest.class

# Step 3: Extract the class
cd /tmp
jar -xf ~/.m2/repository/.../montoya-api-2026.4.jar \
  burp/api/montoya/http/message/requests/HttpRequest.class

# Step 4: Look for static methods
javap -v burp/api/montoya/http/message/requests/HttpRequest.class | grep "public static"
# Results:
#   public static HttpRequest httpRequest()
#   public static HttpRequest httpRequestFromUrl(String)
#   public static HttpRequest httpRequest(HttpService, String)
#   ... etc

# Step 5: See full method signature
javap -v burp/api/montoya/http/message/requests/HttpRequest.class | grep -A 10 "httpRequestFromUrl"
```

**Conclusion:** Use `HttpRequest.httpRequestFromUrl("https://example.com")` to create requests!

---

## Summary

| Step | Command | Purpose |
|------|---------|---------|
| 1 | `find ~/.m2/repository -name "*.jar"` | Locate JAR file |
| 2 | `jar -tf library.jar \| grep Pattern` | Find class in JAR |
| 3 | `jar -xf library.jar path/to/Class.class` | Extract class file |
| 4 | `javap Class.class` | View methods |
| 5 | `javap -v Class.class \| grep pattern` | Search for specific method |

---

## Practice Exercise

Try finding all methods in the `Http` service:

```bash
cd /tmp && \
jar -xf ~/.m2/repository/net/portswigger/burp/extensions/montoya-api/2026.4/montoya-api-2026.4.jar \
  burp/api/montoya/http/Http.class && \
javap burp/api/montoya/http/Http.class
```

What methods does `Http` service provide?

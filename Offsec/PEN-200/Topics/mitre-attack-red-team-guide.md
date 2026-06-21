# MITRE ATT&CK for Red Teamers — Quick Guide

A practical reference for learning ATT&CK efficiently while building red team skills (aligned with PEN-200 / OSCP-style work).

---

## What It Is (30-Second Version)

**MITRE ATT&CK** is a public knowledge base of real-world adversary behavior. It organizes attacks into:

| Layer | Meaning | Example |
|-------|---------|---------|
| **Tactic** | *Why* the adversary does something (goal) | Privilege Escalation |
| **Technique** | *How* they achieve that goal | T1059 — Command and Scripting Interpreter |
| **Sub-technique** | A specific variant | T1059.001 — PowerShell |
| **Procedure** | The actual tools/commands used in the wild | `Invoke-Mimikatz`, Cobalt Strike beacon |

Think of it as a **shared language** between red team, blue team, and leadership—not a checklist of every hack.

---

## Efficient Learning Path (Red Team Focus)

Do not try to memorize all 600+ techniques. Use this order:

### Phase 1 — Learn the map (1–2 sessions)

1. Open [attack.mitre.org](https://attack.mitre.org/) → **Enterprise Matrix**.
2. Read tactics left-to-right (the attack lifecycle).
3. Skim 2–3 techniques per tactic—only names and one-line descriptions.

### Phase 2 — Learn by doing (ongoing)

After every lab box or red team exercise:

1. Pick **one technique** you actually used.
2. Look it up on ATT&CK (e.g., `T1059.001`).
3. Write: tactic → technique → your command/tool → what detection might see it.

### Phase 3 — Build coverage, not memorization (weekly)

1. Choose one tactic (e.g., **Credential Access**).
2. Read its top 5 techniques.
3. For each: know one red team tool/example and one detection idea.

### Phase 4 — Tie to operations (before any engagement)

1. Define **objectives** (e.g., domain admin, data exfil simulation).
2. Draft a **threat profile** (e.g., “ransomware affiliate” or “insider”).
3. Map planned actions to ATT&CK → this becomes your **attack narrative** and report backbone.

**Rule of thumb:** 70% hands-on labs, 30% ATT&CK reading. ATT&CK makes your work *communicable*; labs make you *competent*.

---

## Main Building Blocks

### Matrices (know which one you use)

| Matrix | Use when |
|--------|----------|
| **Enterprise** | Windows/Linux/macOS, AD, cloud workloads — **default for red team** |
| **Mobile** | Android/iOS assessments |
| **ICS** | Industrial / OT environments |

### Tactics (Enterprise) — the attack timeline

```
Recon → Resource Dev → Initial Access → Execution → Persistence
→ Privilege Esc → Defense Evasion → Credential Access → Discovery
→ Lateral Movement → Collection → C2 → Exfil → Impact
```

You will not hit every tactic on every engagement. OSCP-style boxes often cover: Initial Access → Execution → Privilege Esc → (sometimes) Lateral Movement.

### Key ATT&CK artifacts

| Artifact | Red team use |
|----------|----------------|
| **Technique page** | Description, platforms, permissions needed, mitigations, detections |
| **Groups (Gxxxx)** | Real APT behavior to emulate |
| **Software (Sxxxx)** | Tools mapped to techniques (Cobalt Strike, Mimikatz, etc.) |
| **Mitigations (Mxxxx)** | What defenders *should* have—helps you plan bypasses ethically |
| **Data sources** | What logs/Sensors blue team needs—useful for purple team debriefs |

### ATT&CK Navigator

Browser tool to **color-code techniques** you plan to test or have tested.

- Create a layer → mark techniques Used / Planned / Not in scope.
- Export JSON for reports and retesting.

URL: [github.com/mitre-attack/attack-navigator](https://github.com/mitre-attack/attack-navigator)

---

## Red Team Use Cases

| Use case | How ATT&CK helps | Example |
|----------|------------------|---------|
| **Scope & rules of engagement** | Define allowed tactics/techniques | “No Impact (T1486 ransomware). Credential Access allowed.” |
| **Attack planning** | Structure TTPs before execution | Map phishing → execution → persistence → DA path |
| **Threat emulation** | Copy a known group’s behavior | Emulate APT29: T1566.001 spearphish → T1059.001 PowerShell |
| **Reporting** | Executive-friendly narrative | “We achieved Lateral Movement (T1021.002) via SMB” |
| **Detection validation** | Prove whether controls catch behavior | Run T1003.001; check if LSASS access alerted |
| **Purple team** | Shared vocabulary for debrief | “We used T1558.003; you had no alert on SPN abuse” |
| **Tool selection** | Pick tools that match desired TTPs | Need stealth cred access? Review T1003 sub-techniques |
| **Gap analysis** | Show what was / wasn’t tested | Navigator heatmap of covered vs. uncovered techniques |

---

## Examples Mapped to Common Red Team / Lab Actions

### Example 1 — Web shell on a Linux box (OSCP-style)

| Step | Your action | ATT&CK mapping |
|------|-------------|----------------|
| Find SQLi | Manual testing | T1190 — Exploit Public-Facing Application |
| Upload shell | `<?php system($_GET['cmd']); ?>` | T1505.003 — Web Shell |
| Run commands | `bash -i` reverse shell | T1059.004 — Unix Shell |
| Read `/etc/shadow` | Credential dump | T1003.008 — `/etc/passwd` and `/etc/shadow` |
| SUID exploit | `./find -exec ...` | T1068 — Exploitation for Privilege Escalation |

**Report sentence:** *Initial Access via T1190, Execution through T1059.004, Privilege Escalation via T1068.*

---

### Example 2 — Windows / Active Directory path

| Step | Your action | ATT&CK mapping |
|------|-------------|----------------|
| Kerberoast | `GetUserSPNs.py` / Rubeus | T1558.003 — Kerberoasting |
| Crack hash | Hashcat mode 13100 | (Procedure under Credential Access) |
| Pass-the-Hash | `impacket-wmiexec` | T1550.002 — Pass the Hash |
| Admin share | `C$` via stolen hash | T1021.002 — SMB/Windows Admin Shares |
| DCSync | `secretsdump.py` | T1003.006 — DCSync |

**Report sentence:** *Credential Access (T1558.003) enabled Lateral Movement (T1021.002) and domain credential theft (T1003.006).*

---

### Example 3 — Phishing simulation (corporate red team)

| Step | Your action | ATT&CK mapping |
|------|-------------|----------------|
| Send targeted email | Fake IT reset link | T1566.001 — Spearphishing Attachment/Link |
| User runs macro | Office doc | T1204.002 — Malicious File |
| Download payload | HTTPS pull | T1105 — Ingress Tool Transfer |
| C2 beacon | Cobalt Strike / Sliver | T1071.001 — Web Protocols |
| Persist | Scheduled task | T1053.005 — Scheduled Task |

---

### Example 4 — Defense evasion (know the labels)

| Action | ATT&CK |
|--------|--------|
| Obfuscate PowerShell | T1027 — Obfuscated Files or Information |
| Disable AMSI (lab only) | T1562.001 — Disable or Modify Tools |
| Clear event logs | T1070.001 — Clear Windows Event Logs |
| Rename binary to `svchost.exe` | T1036.003 — Rename System Utilities |

Use these labels in debriefs so blue team knows *what behavior* to tune detections for—not just “the red team ran a script.”

---

## Weekly Study Template (30–45 min)

Copy into your notes after a lab session:

```
Date:
Target / lab:
Objective:

Techniques used:
- T____ — (name) — command/tool:
- T____ — (name) — command/tool:

Tactic flow (one line):
Initial Access → ... → Impact

What would detect this?
-

What mitigation exists on ATT&CK page?
-

Next technique to study in this tactic:
-
```

---

## What “Competent” Looks Like

You do **not** need to recite every technique ID. You **do** need to:

- [ ] Name all 14 Enterprise tactics in order (roughly).
- [ ] For any technique you use, find its page in under 60 seconds.
- [ ] Map a full lab attack path to at least 5 technique IDs.
- [ ] Explain one technique to a non-technical stakeholder using tactic language.
- [ ] Use Navigator to show coverage for a mock engagement.
- [ ] Read mitigations/detections on a technique and describe one bypass *concept* (in authorized context).

---

## Recommended Resources

| Resource | Purpose |
|----------|---------|
| [attack.mitre.org](https://attack.mitre.org/) | Official matrix and technique pages |
| [ATT&CK Navigator](https://mitre-attack.github.io/attack-navigator/) | Visual planning and reporting |
| [MITRE ATT&CK Training](https://mitre-attack.github.io/attack-training/) | Free official modules |
| [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team) | Safe technique tests mapped to ATT&CK |
| [MITRE Cyber Analytics Repository (CAR)](https://car.mitre.org/) | Analytics tied to techniques |

**Atomic Red Team tip:** After rooting a box, find one matching atomic test for a technique you used—run it in a home lab to see what telemetry it generates.

---

## Common Mistakes to Avoid

1. **Memorizing IDs without doing labs** — IDs mean nothing without execution context.
2. **Treating ATT&CK as an engagement checklist** — Real ops are opportunistic; map what you *did*, not every box on the matrix.
3. **Ignoring sub-techniques** — `T1059` is vague; `T1059.001` (PowerShell) is what defenders detect.
4. **Forgetting procedures** — Two techniques may share an ID path but different tools leave different artifacts.
5. **Skipping mitigations/detections** — Red team competence includes knowing how your actions appear to defenders.

---

## Connection to PEN-200 / OSCP

| PEN-200 topic | Primary ATT&CK tactics |
|---------------|------------------------|
| Info gathering | Reconnaissance, Discovery |
| Web attacks / SQLi | Initial Access, Execution |
| Client-side / password attacks | Initial Access, Credential Access |
| Linux/Windows privesc | Privilege Escalation |
| Pivoting / tunneling | Command and Control, Lateral Movement |
| Active Directory | Credential Access, Lateral Movement, Persistence |

Add one row to your session log: **“ATT&CK techniques today.”** After 20–30 lab sessions, you will naturally know the framework without flashcard drudgery.

---

*Last updated: June 2025 — verify technique IDs on attack.mitre.org as the framework evolves.*

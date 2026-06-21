# PEN-200 Daily Practice Plan

A structured 12-week plan to work through PEN-200 consistently. Adjust pace as needed—consistency matters more than speed.

**Target commitment:** 10–15 hours per week (~90 minutes on weekdays, one 4-hour block on the weekend)

---

## Daily Session Template

Use this structure every time you sit down to study.

### Before you start (5 min)

- [ ] Write today's goal (one sentence)
- [ ] Open your notes and yesterday's session log
- [ ] Close distractions; set a timer

### During the session

| Block | Time | Activity |
|-------|------|----------|
| Warm-up | 10 min | Review yesterday's commands or one checklist |
| Learn | 20–30 min | Read/watch one module section (weekdays only) |
| Lab | 45–90 min | Hands-on exercises or active box work |
| Cool-down | 10 min | Update notes and session log |

### After every session (5 min)

Answer these in your notes:

1. What did I accomplish?
2. What am I stuck on?
3. What is the first thing I will do next session?

---

## Weekly Schedule

| Day | Duration | Focus |
|-----|----------|-------|
| Monday | 90 min | New module section + related lab exercise |
| Tuesday | 90 min | Continue lab work from Monday |
| Wednesday | 60 min | Review notes; redo one technique that failed |
| Thursday | 90 min | New module section + lab exercise |
| Friday | 60 min | Light lab or catch-up on the week's topic |
| Saturday | 4 hours | Deep lab block (one box or challenge lab segment) |
| Sunday | 30–60 min | Weekly review; plan next week; rest if needed |

**Weekly rule:** 70% lab time, 30% reading/watching.

---

## 12-Week Roadmap

### Phase 1 — Foundations (Weeks 1–3)

**Goal:** Build enumeration habits and basic attack workflow.

| Week | Course focus | Lab focus | Weekly deliverable |
|------|--------------|-----------|-------------------|
| 1 | Course intro, networking refresh, info gathering | Port scanning, service enum, note-taking setup | Personal enum checklist (v1) |
| 2 | Vulnerability scanning, web app intro | Nmap scripts, basic web dir/file discovery | Web enum checklist (v1) |
| 3 | Common web attacks, SQL injection | Manual SQLi, basic web exploits in lab | One full box write-up (foothold → user) |

**Daily habit this phase:** Run the same baseline enum on every new target before guessing an exploit.

---

### Phase 2 — Core Skills (Weeks 4–6)

**Goal:** Exploit public code, crack passwords, and chain techniques.

| Week | Course focus | Lab focus | Weekly deliverable |
|------|--------------|-----------|-------------------|
| 4 | Client-side attacks, locating public exploits | Searchsploit, modify/run exploits safely | Exploit workflow notes (find → assess → run) |
| 5 | Fixing exploits, AV evasion basics | Cross-compile/port one public exploit | Updated cheat sheet for compile errors |
| 6 | Password attacks, Metasploit intro | Hash cracking, basic MSF modules | Password attack decision tree |

**Daily habit this phase:** Time-box rabbit holes to 45–60 minutes, then pivot enumeration.

---

### Phase 3 — Privilege Escalation & Movement (Weeks 7–9)

**Goal:** Reliably escalate on Linux and Windows; understand pivoting.

| Week | Course focus | Lab focus | Weekly deliverable |
|------|--------------|-----------|-------------------|
| 7 | Linux privilege escalation | LinPEAS/manual checks, SUID, cron, paths | Linux privesc checklist (your version) |
| 8 | Windows privilege escalation | WinPEAS/manual checks, services, tokens | Windows privesc checklist (your version) |
| 9 | Port redirection, SSH tunneling, DPI tunneling | chisel, ligolo, ssh -L/-R/-D in lab | Pivoting quick-reference sheet |

**Daily habit this phase:** After every foothold, run privesc enum before trying random exploits.

---

### Phase 4 — Active Directory & Challenge Labs (Weeks 10–12)

**Goal:** AD basics and exam-style endurance.

| Week | Course focus | Lab focus | Weekly deliverable |
|------|--------------|-----------|-------------------|
| 10 | AD intro, enumeration, auth attacks | BloodHound/enum, kerberoasting basics | AD enum checklist |
| 11 | AD lateral movement, assembling the pieces | Multi-host lab paths | One challenge lab segment completed |
| 12 | Challenge labs ("Try Harder") | Full challenge lab under timed conditions | Mock report for one completed lab |

**Daily habit this phase:** Practice explaining your attack path out loud after each session.

---

## Daily Checklists

### Enumeration baseline (run on every new target)

- [ ] `nmap` (or rustscan + nmap) — ports and versions
- [ ] Web: directories, tech stack, source/comments, vhosts
- [ ] SMB/NFS/FTP/SNMP if present
- [ ] Default creds and anonymous access checks
- [ ] Search for known CVEs on identified versions

### Linux privesc (after initial access)

- [ ] `id`, `uname -a`, `sudo -l`
- [ ] SUID/SGID binaries, writable paths in `$PATH`
- [ ] Cron jobs, capabilities, Docker/socket exposure
- [ ] Interesting files: `/etc/passwd`, configs, history, backups

### Windows privesc (after initial access)

- [ ] `whoami /all`, `systeminfo`
- [ ] Unquoted service paths, weak service permissions
- [ ] AlwaysInstallElevated, stored creds, tokens
- [ ] Scheduled tasks, registry autologon, misconfigured ACLs

### End-of-week review (Sunday)

- [ ] Update personal cheat sheet with new commands
- [ ] Redo one technique without looking at notes
- [ ] Identify one weak area for next week
- [ ] Set Monday's goal in writing

---

## Session Log Template

Copy this into your notes for each session:

```
Date:
Duration:
Week / Phase:
Goal:

Done:
- 
- 

Stuck on:

Next session starts with:

Commands worth keeping:
-
```

---

## Exam Readiness Milestones

Do not schedule the exam until you can check most of these:

- [ ] Root medium-difficulty lab boxes without writeups
- [ ] Explain your attack path clearly (foothold → privesc → root)
- [ ] Linux and Windows privesc from your own checklists
- [ ] Set up pivoting/tunneling when a box requires it
- [ ] Complete at least 2–3 challenge labs independently
- [ ] Write a concise report under time pressure

---

## Rules to Protect Momentum

1. **One box at a time** — finish or fully document a blocker before switching.
2. **No writeups until stuck** — struggle first; hints second; writeups last.
3. **Rebuild once** — redo a rooted box without notes within a week.
4. **Sleep on hard problems** — stepping away often unlocks progress.
5. **Consistency over intensity** — daily 90 minutes beats random 10-hour marathons.

---

## Quick Reference: What to Do When Stuck

1. Re-read your enum output — something was missed.
2. Google the exact service version + " exploit" / " default creds".
3. Check alternate ports, vhosts, and UDP services.
4. Ask: "What would a patient tester try next?" (not "what tool should I install?").
5. After 60 minutes with no progress, take a 15-minute break and re-enumerate.

---

*Adjust weeks up or down based on your schedule. If you fall behind, shorten reading and protect lab time.*

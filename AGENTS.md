<!-- BEGIN:wave-safety-rules -->
# WAVE SAFETY — Run these checks every time, no exceptions

## 0. Startup (copy-paste this block at the start of EVERY wave task)
```bash
git config user.email noreply@anthropic.com && git config user.name Claude
git checkout claude/swarm-50-agent-architecture-3l6cno
git pull origin claude/swarm-50-agent-architecture-3l6cno
git branch --show-current   # MUST print: claude/swarm-50-agent-architecture-3l6cno
```

## 1. Before touching Sidebar.tsx — check for existing icon
```bash
grep -c "^function IconYourNewName" components/Sidebar.tsx
# 0 → safe to add   |   1+ → REUSE existing, do NOT add again
```

## 2. After editing Sidebar.tsx — verify zero duplicates
```bash
grep "^function Icon" components/Sidebar.tsx | awk -F'[{ ]' '{print $3}' | sort | uniq -d
# Must return EMPTY. If not → remove the earlier duplicate before committing.
```

## 3. Before every commit — working tree must be clean
```bash
git status --short
# ?? lines → git add + commit those files first
# M lines  → stage and include in commit
```

## 4. Sidebar.tsx rule — ONE agent at a time
Never edit Sidebar.tsx in parallel with another running agent.
Always `git pull` immediately before editing Sidebar.tsx.

## 5. Commit immediately after each file group is done
Do NOT batch everything at the end. Commit engines → commit routes → commit sidebar → commit dashboards.
<!-- END:wave-safety-rules -->

<!-- BEGIN:nextjs-agent-rules -->
# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.
<!-- END:nextjs-agent-rules -->

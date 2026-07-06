# Audit Report Template (Phase 2)

Use this exact structure for the audit report.

```
================================
ARCHITECTURE AUDIT REPORT
================================
Project: <project-name>
Stack:   <language> + <framework>
Files:   <N> analyzed | ~<LOC> lines of code

## Summary
CRITICAL: <n> | HIGH: <n> | MEDIUM: <n> | LOW: <n>

## Findings

### [CRITICAL] <Title>
File: <path>:<start>-<end> (or single line)
Description: <what was found>
Impact: <why it matters>
Recommendation: <how to fix>

### [HIGH] <Title>
...

### [MEDIUM] <Title>
...

### [LOW] <Title>
...

================================
Total: <N> findings
================================

Phase 2 complete. Proceed with refactoring (Phase 3)? [y/n]
```

## Rules

1. Order findings: CRITICAL → HIGH → MEDIUM → LOW
2. Every finding MUST have exact file path and line numbers
3. Minimum 5 findings per project
4. Include at least one CRITICAL or HIGH
5. Include deprecated API findings when applicable (AP10)
6. **STOP** after printing the prompt — do not modify files until user confirms

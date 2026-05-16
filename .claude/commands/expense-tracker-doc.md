---
description: Generate and maintain comprehensive documentation from code
argument-hint: [--api or --readme]
allowed-tools: Bash(ls:*), Bash(cat:*), Bash(test:*), Bash(grep:*), Bash(find:*)
---


Generate and maintain documentation from code, keeping it in sync with implementation.

## Usage Examples

**Basic documentation generation:**
```
/expense-report-docs
```

**Generate API documentation:**
```
/expense-report-docs --api
```

**Check documentation coverage:**
```
/expense-report-docs --check
```

**Generate README:**
```
/expense-report-docs --readme
```

**Help and options:**
```
/expense-report-docs --help

## Implementation

if $ARGUMENTS contains "help" or "--help":
Display this usage information and exit.

Parse documentation options from $ARGUMENTS (--genarate, --api, --readme, --check, or specific module/file).

##1. Analyze Current Documentation

Check existing documentation:

```
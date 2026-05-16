---
description: Run complete workflow - refactor code then generate documentation
argument-hint: [file-path]
allowed-tools: Bash(cat:*), Bash(python:*), Bash(pytest:*), Bash(ls:*), Bash(grep:*), Bash(find:*)
---

# Full workflow: Refactor + Documentation

Excute the complete development workflow for: $ARGUMENTS

if $ARGUMENTS is empty, process the entire codebase.

## Workflow Steps

### Phase 1: Code Refactoring
run the below slash command
`/expense-tracker-code-refactor [file]` | Refactor Python code for better quality |

## Phase 2: Documentation Generation
Run the below slash command sequentially
`/expense-tracker-doc --check` | Check documentation coverage |
`/expense-tracker-doc` | Generate all documentation |
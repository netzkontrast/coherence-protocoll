# Claude Code Setup - Coherence Protocol

This project is configured with Claude Code customizations to enhance your development workflow with specialized agents, commands, and skills.

## Overview

The Coherence Protocol project uses Claude Code to provide:
- **Specialized agents** for complex technical tasks
- **Custom commands** for streamlined workflows
- **Integrated skills** for document generation, PDF handling, and more
- **Smart automation** for commits, documentation, and project management

## Custom Agents

Agents are specialized AI assistants available through the `Task` tool. Invoke them for complex, multi-step tasks:

### context-manager
**Use case:** Complex projects requiring coordination across multiple sessions

Maintains coherent state across agent interactions, capturing context, distributing it to other agents, and managing project memory. Activates proactively for long-running tasks and multi-agent workflows.

**Available tools:** Read, Write, Edit, TodoWrite

### nextjs-architecture-expert
**Use case:** Next.js applications, App Router, performance optimization

Master of Next.js best practices, server components, and framework optimization. Use proactively for architecture decisions and migration strategies.

**Available tools:** Read, Write, Edit, Bash, Grep, Glob

### prompt-engineer
**Use case:** Building AI features, optimizing prompts for LLMs

Expert in prompt optimization and AI system design. Use proactively when crafting system prompts or improving agent performance.

**Available tools:** Read, Write, Edit

### task-decomposition-expert
**Use case:** Complex multi-step projects requiring different capabilities

Specialist in breaking down large goals into manageable tasks and orchestrating workflows using multiple tools and ChromaDB integration.

**Available tools:** Read, Write

### typescript-pro
**Use case:** Advanced TypeScript, complex type systems, migrations

Writes idiomatic TypeScript with strict typing, advanced type system features, and modern patterns. Use proactively for type optimization.

**Available tools:** Read, Write, Edit, Bash

## Custom Commands

Commands are slash commands that execute workflows. Use them with `/command-name`:

### /commit
**Create well-formatted commits with conventional commit format and emoji**

Syntax: `/commit [message]` or `/commit [message] | --no-verify | --amend`

Features:
- Runs pre-commit checks (lint, build, generate docs)
- Automatically stages changes if needed
- Analyzes diffs to detect multiple logical changes
- Suggests breaking commits into smaller ones
- Creates conventional commit format with emoji

Example:
```
/commit "Add new authentication flow"
/commit "Update docs" --no-verify
```

### /ultra-think
**Deep analysis and problem solving with multi-dimensional thinking**

Syntax: `/ultra-think [problem or question to analyze]`

Features:
- Multi-dimensional analysis
- Comprehensive problem exploration
- Deep reasoning and solutions

Example:
```
/ultra-think "How to optimize database queries in our app?"
```

### /todo
**Manage project todos in todos.md file**

Syntax: `/todo [action] [task-description]`

Actions: `add | complete | remove | list`

Example:
```
/todo add "Implement new feature X"
/todo list
/todo complete "Implement new feature X"
```

### /create-architecture-documentation
**Generate comprehensive architecture documentation**

Syntax: `/create-architecture-documentation [framework]` with options:
- `--c4-model`: C4 model diagrams
- `--arc42`: Arc42 architecture documentation
- `--adr`: Architecture Decision Records
- `--plantuml`: PlantUML diagrams
- `--full-suite`: Complete documentation suite

Example:
```
/create-architecture-documentation nextjs --full-suite
```

### /update-docs
**Systematically update project documentation**

Syntax: `/update-docs [doc-type]` with options:
- `--implementation`: Update implementation status
- `--api`: Update API documentation
- `--architecture`: Update architecture docs
- `--sync`: Synchronize content
- `--validate`: Validate documentation

Example:
```
/update-docs --implementation --sync
```

### /workflow-orchestrator
**Orchestrate complex automation workflows**

Syntax: `/workflow-orchestrator [workflow-name]` with actions:
- `create`: Create new workflow
- `run`: Execute workflow
- `schedule`: Schedule workflow
- `monitor`: Monitor execution

Example:
```
/workflow-orchestrator my-workflow run
```

## Integrated Skills

Skills provide specialized capabilities for document and file handling:

### artifacts-builder
Create elaborate multi-component HTML artifacts using React, Tailwind CSS, and shadcn/ui. Use for complex interactive documentation and visualizations.

### docx
Work with Word documents (.docx files):
- Create new documents
- Modify and edit content
- Handle tracked changes and comments
- Preserve formatting

### pdf-anthropic
Comprehensive PDF manipulation:
- Extract text and tables
- Fill PDF forms
- Merge/split documents
- Generate new PDFs

### theme-factory
Apply or create themes for artifacts:
- 10 pre-set themes available
- Custom theme generation
- Style documents, slides, and reports

### skill-creator
Guide for creating new skills to extend Claude's capabilities.

## Configuration

### Settings (`.claude/settings.json`)

The project includes custom configuration:

```json
{
  "statusLine": {
    "type": "command",
    "command": "python .claude/scripts/context-monitor.py"
  },
  "env": {
    "CLAUDE_CODE_MAX_OUTPUT_TOKENS": "8000",
    "DISABLE_NON_ESSENTIAL_MODEL_CALLS": "1",
    "DISABLE_COST_WARNINGS": "1"
  }
}
```

- **Status line:** Displays context monitoring information
- **Environment variables:** Configure token limits and model behavior

### Context Monitoring

The project includes a Python script (`.claude/scripts/context-monitor.py`) that monitors context usage and provides real-time feedback in the status line.

## Usage Tips

1. **For complex tasks:** Use the `context-manager` agent to maintain state across multiple interactions
2. **For framework-specific work:** Use `nextjs-architecture-expert` or `typescript-pro` based on your needs
3. **For commits:** Use `/commit` command instead of manual git operations
4. **For planning:** Use `/ultra-think` for deep analysis or `/todo` for tracking tasks
5. **For documentation:** Use `/create-architecture-documentation` or `/update-docs` commands

## Development Branch

When working on features, you develop on designated branches following the pattern:
- Branch naming: `claude/[feature-name]-[session-id]`
- Always create pull requests from your working branch
- Keep the main branch stable

## Getting Help

For more information about Claude Code:
- Use `/help` in Claude Code
- Check the official documentation: https://github.com/anthropics/claude-code
- Report issues at: https://github.com/anthropics/claude-code/issues

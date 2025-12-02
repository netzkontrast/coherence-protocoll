# Coherence Protocol - AI Coding Agent Instructions

## Project Overview

The **Coherence Protocol** is a comprehensive Claude Code configuration framework that provides reusable agents, commands, and skills to enhance AI-assisted development workflows. This is a meta-project designed to standardize and extend Claude's capabilities across different development contexts.

## Architecture

### Three-Tier Component System

1. **Agents** (`.claude/agents/`) - Specialized AI assistants for complex domains
   - Each agent has a defined purpose, tool access, and model configuration
   - Agents are invoked for multi-step, context-heavy tasks
   - Examples: `context-manager`, `typescript-pro`, `nextjs-architecture-expert`

2. **Commands** (`.claude/commands/`) - Workflow automations (slash commands)
   - Execute workflows triggered by `/command-name` syntax
   - Can call external processes (git, build tools, scripts)
   - Examples: `/commit`, `/update-docs`, `/ultra-think`

3. **Skills** (`.claude/skills/`) - Specialized capabilities
   - Provide domain-specific functions (PDF processing, document generation)
   - Self-contained modules with scripts and documentation
   - Examples: `pdf-anthropic`, `artifacts-builder`, `docx`, `theme-factory`

### Key Directories

- `.claude/agents/` - Agent definitions and specializations
- `.claude/commands/` - Command workflow definitions  
- `.claude/skills/` - Reusable capability modules
- `.claude/scripts/` - Shared utility scripts (Python/Bash)
- `.claude/settings.json` - Framework configuration
- `Claude.md` - User-facing documentation

## Critical Developer Workflows

### Building & Verification
- **Build task**: `msbuild /property:GenerateFullPaths=true /t:build`
  - Defined in workspace tasks configuration
  - Run via `run_task` tool with label "build"

### Creating Commits
- Use `/commit` command instead of manual git operations
- Automatically runs: `pnpm lint`, `pnpm build`, `pnpm generate:docs`
- Analyzes diffs to suggest splitting into atomic commits
- Enforces conventional commit format with emoji

### Documentation Updates
- Use `/update-docs` command for systematic documentation changes
- Use `/create-architecture-documentation` for generating architecture docs
  - Supports C4 model, Arc42, ADR, PlantUML, full-suite options

## Project-Specific Patterns

### Agent Specialization Pattern
Each agent follows a consistent structure in its markdown file:
```yaml
---
name: [agent-name]
description: [Purpose and when to use]
tools: [Comma-separated tool access list]
model: [Model name, often "opus"]
---
```

Example: `typescript-pro` agent uses strict typing and modern TypeScript patterns. When working with complex type systems or migrations, invoke this agent proactively.

### Command Workflow Pattern
Commands are defined in `.claude/commands/` with:
- **allowed-tools**: Git commands, Bash operations
- **argument-hint**: Expected parameters
- **description**: Command purpose
- Implementation that can read repository state, run processes

Example: `/commit` reads git status, stages files, runs checks, then creates formatted commits.

### Skill Encapsulation Pattern
Skills in `.claude/skills/` provide:
- `SKILL.md` - Public interface documentation
- `LICENSE.txt` - Terms and restrictions
- `scripts/` - Implementation utilities
- Supporting documentation (reference.md, forms.md, etc.)

## Integration Points

### Git Operations
- All git operations should use `/commit` command, not direct git calls
- Pre-commit hooks can be bypassed with `--no-verify` flag
- Conventional commit format required: `<emoji> <type>: <description>`

### External Commands
- PDF processing: Use `pdf-anthropic` skill (pypdf, reportlab, etc.)
- Document generation: Use `docx` skill for Word documents
- Visualization: Use `artifacts-builder` for interactive HTML/React components
- Theming: Use `theme-factory` for consistent styling

### Configuration Files
- `.claude/settings.json` - Global framework settings
- `.claude/settings.local.json` - Local overrides (permissions, environment)
  - Currently restricts Bash to git config and cat operations

## Context Management Strategy

For complex multi-session work:
1. Use `context-manager` agent proactively to maintain coherence
2. Agent extracts decisions, patterns, integration points
3. Generates "Quick Context" summaries (< 500 tokens) for subsequent agents
4. Maintains rolling memory of recent changes and blockers

This is critical for long-running projects needing coordination across multiple AI agents.

## Common Use Cases & Recommended Workflows

| Task | Recommended Tool(s) |
|------|-------------------|
| Add new feature | `task-decomposition-expert` + `context-manager` |
| Debug TypeScript | `typescript-pro` agent |
| Optimize Next.js app | `nextjs-architecture-expert` agent |
| Complex commit | `/commit` command |
| Deep analysis | `/ultra-think` command |
| Track work items | `/todo` command |
| Generate docs | `/create-architecture-documentation` command |
| Process PDF | `pdf-anthropic` skill |
| Create interactive docs | `artifacts-builder` skill |

## Key Files to Understand

- `Claude.md` - Complete feature catalog and usage guide
- `.claude/settings.json` - Framework configuration and status monitoring
- `.claude/agents/*.md` - Individual agent definitions
- `.claude/commands/*.md` - Command implementations
- `.claude/skills/*/SKILL.md` - Skill interfaces

## Conventions

- Branch naming: `claude/[feature-name]-[session-id]`
- Commit messages: Conventional format with emoji (✨ feat, 🐛 fix, 📚 docs, etc.)
- Documentation: Keep `.github/copilot-instructions.md` updated with patterns and workflows
- Configuration: Use `.claude/settings.local.json` for local permission overrides

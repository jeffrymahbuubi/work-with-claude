# Claude Code Boilerplate

A starter template for working with Claude Code, complete with custom agents, skills, and environment setup scripts.

## Table of Contents

- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Using Custom Agents](#using-custom-agents)
  - [Creating an Agent](#creating-an-agent)
  - [Invoking an Agent](#invoking-an-agent)
- [Using Custom Skills](#using-custom-skills)
  - [Creating a Skill](#creating-a-skill)
  - [Invoking a Skill](#invoking-a-skill)
- [Using Custom Commands](#using-custom-commands)
  - [Creating a Command](#creating-a-command)
  - [Invoking a Command](#invoking-a-command)
- [Environment Variables](#environment-variables)
  - [Setup](#setup)
  - [Make Script Executable](#make-script-executable)
- [CLAUDE.md - Project Instructions](#claudemd---project-instructions)
- [Local Permissions](#local-permissions)
- [MCP Server Setup](#mcp-server-setup)
  - [Available MCP Servers](#available-mcp-servers)
  - [Security Best Practices](#security-best-practices)
  - [Example .env Configuration](#example-env-configuration)
  - [Verifying MCP Server Installation](#verifying-mcp-server-installation)
  - [Removing MCP Servers](#removing-mcp-servers)
- [Customizing for Your Project](#customizing-for-your-project)
- [Best Practices](#best-practices)
  - [Agents](#agents)
  - [Skills](#skills)
  - [Commands](#commands)
  - [Environment Variables](#environment-variables-1)
- [Troubleshooting](#troubleshooting)
- [Examples](#examples)
- [Resources](#resources)
- [License](#license)

## Quick Start

1. **Clone or copy this repository** to your project directory
2. **Create your `.env` file** from the example:
   ```bash
   cp .env.example .env
   ```
3. **Edit `.env`** with your environment variables (API keys, tokens, etc.)
4. **Launch Claude Code** with environment variables:
   ```bash
   ./scripts/claude-with-env.sh
   ```

## Repository Structure

```
.
├── .claude/                      # Claude Code configuration
│   ├── agents/                   # Custom agents
│   │   └── example-agent.md      # Example agent template
│   ├── skills/                   # Custom skills
│   │   ├── example-skill/        # Example skill template
│   │   │   └── SKILL.md
│   │   ├── mermaid-diagram-specialist/  # Mermaid diagram creation
│   │   │   └── SKILL.md
│   │   └── xlsx/                 # Excel file operations
│   │       └── SKILL.md
│   ├── commands/                 # Custom commands
│   │   └── example-command.md    # Example command template
│   └── settings.local.json       # Local permissions settings
├── scripts/                      # Utility scripts
│   ├── claude-with-env.sh        # Launch Claude with .env variables
│   └── start_jupyter_server.sh   # Start Jupyter server for MCP integration
├── .env.example                  # Example environment variables
├── .gitignore                    # Git ignore rules
├── CLAUDE.md                     # Project-specific Claude instructions
└── README.md                     # This file
```

## Using Custom Agents

Agents are specialized AI assistants with specific expertise and tools. They live in `.claude/agents/`.

### Creating an Agent

Create a new `.md` file in `.claude/agents/` with frontmatter:

```markdown
---
name: my-agent
description: "Use this agent when you need to [describe use case]"
tools: Bash, Read, Write, Grep, Glob
model: sonnet
color: blue
---

# Agent Instructions

[Your agent's system prompt and instructions go here]
```

### Invoking an Agent

Use the `Task` tool with `subagent_type` matching your agent's name:

```
I need to analyze this data with my custom agent
```

Or Claude will automatically suggest using your agent when the task matches its description.

## Using Custom Skills

Skills are reusable capabilities that can be invoked with slash commands. They live in `.claude/skills/`.

### Creating a Skill

1. Create a folder in `.claude/skills/` with your skill name
2. Add a `SKILL.md` file with frontmatter:

```markdown
---
name: my-skill
category: dev
description: Brief description of what this skill does
usage: When to use this skill
input: What input this skill needs
output: What output this skill produces
---

# Skill Instructions

[Your skill's instructions and workflow go here]
```

### Invoking a Skill

Use the skill with a slash command:

```
/my-skill
```

Or mention it in conversation and Claude will offer to invoke it.

## Using Custom Commands

Commands are simple shortcuts for common tasks. They live in `.claude/commands/`.

### Creating a Command

Create a `.md` file in `.claude/commands/`:

```markdown
---
name: example
description: Brief description of what this command does
---

# Command Instructions

[Instructions for what Claude should do when this command is invoked]
```

### Invoking a Command

Use the command with a slash:

```
/example
```

## Environment Variables

The `claude-with-env.sh` script loads environment variables from `.env` before launching Claude Code.

### Setup

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your values:
   ```bash
   # API Keys
   ANTHROPIC_API_KEY=your_key_here
   OPENAI_API_KEY=your_key_here

   # Project-specific variables
   DATABASE_URL=your_database_url
   ```

3. Launch Claude with environment variables:
   ```bash
   ./scripts/claude-with-env.sh
   ```

### Make Script Executable

If you get a permission error:

```bash
chmod +x scripts/claude-with-env.sh
```

## CLAUDE.md - Project Instructions

The `CLAUDE.md` file provides project-specific context and instructions to Claude Code. This is loaded automatically when Claude works in your project.

Use it to document:
- Project structure and conventions
- How to run tests and scripts
- Important gotchas or requirements
- Repository layout
- Coding standards

## Local Permissions

The `.claude/settings.local.json` file configures auto-approved permissions for specific tools:

```json
{
  "permissions": {
    "allow": [
      "mcp__github__get_file_contents",
      "mcp__filesystem__read_file"
    ]
  }
}
```

Add tool names to the `allow` array to skip permission prompts for those tools.

## MCP Server Setup

Model Context Protocol (MCP) servers extend Claude Code's capabilities by providing additional tools and context. Here's how to set up commonly used MCP servers with project-level scope.

### Available MCP Servers

#### filesystem

Provides file system access to a specific project directory.

**Setup Command:**
```bash
claude mcp add filesystem --scope project -- npx -y \
  @modelcontextprotocol/server-filesystem \
  /path/to/your/project
```

Replace `/path/to/your/project` with your actual project path. This restricts the server's access to that single directory.

#### fetch

Enables web fetching capabilities via HTTP requests.

**Setup Command:**
```bash
claude mcp add fetch --scope project -- uvx mcp-server-fetch
```

#### sequentialthinking

Provides structured thinking capabilities for complex problem-solving.

**Setup Command:**
```bash
claude mcp add sequentialthinking --scope project -- npx -y \
  @modelcontextprotocol/server-sequential-thinking
```

**Note:** The correct package name uses hyphens: `@modelcontextprotocol/server-sequential-thinking`

#### context7

Provides context management with API key support.

**Setup Command:**
```bash
claude mcp add context7 \
  --env CONTEXT7_API_KEY='${CONTEXT7_API_KEY}' \
  --scope project \
  -- npx -y @upstash/context7-mcp
```

**Important:**
- Add `CONTEXT7_API_KEY` to your `.env` file
- The API key is resolved at runtime when Claude Code starts

#### jupyter-mcp-server

Provides Jupyter notebook integration, allowing Claude to execute code, analyze data, and work with Jupyter notebooks directly.

**Prerequisites:**
1. Have Jupyter installed in your environment
2. Start the Jupyter server before using the MCP server

**Step 1: Start Jupyter Server**

Use the provided script to start JupyterLab with the required configuration:

```bash
./scripts/start_jupyter_server.sh
```

**Step 2: Configure the MCP Server**

Add the following to your `.mcp.json` or use the setup command:

```json
"jupyter-mcp-server": {
  "type": "stdio",
  "command": "uvx",
  "args": [
    "jupyter-mcp-server"
  ],
  "env": {
    "JUPYTER_URL": "http://localhost:8888",
    "JUPYTER_TOKEN": "my_secure_token_123",
    "DOCUMENT_ID": "",
    "ALLOW_IMG_OUTPUT": "true"
  }
}
```

**Setup Command (Alternative):**
```bash
claude mcp add jupyter-mcp-server \
  --env JUPYTER_URL='http://localhost:8888' \
  --env JUPYTER_TOKEN='${JUPYTER_TOKEN}' \
  --env DOCUMENT_ID='' \
  --env ALLOW_IMG_OUTPUT='true' \
  --scope project \
  -- uvx jupyter-mcp-server
```

**Important:**
- Add `JUPYTER_TOKEN` to your `.env` file
- The token must match the one used when starting Jupyter server
- Ensure Jupyter server is running before using this MCP server
- Set `ALLOW_IMG_OUTPUT` to `true` to enable image rendering in responses

**Customizing the Jupyter Script:**

Edit `scripts/start_jupyter_server.sh`:
1. Update the project directory path
2. Modify the token to match your `.env` configuration
3. Adjust port if needed (default: 8888)
4. Enable/disable virtual environment activation

### Security Best Practices

- Store all API keys and sensitive credentials in `.env`
- Use `--env` flag to reference environment variables: `--env VAR_NAME='${VAR_NAME}'`
- Never hardcode API keys directly in setup commands
- Keep `.env` out of version control (already in `.gitignore`)

### Example .env Configuration

```bash
# MCP Server API Keys
CONTEXT7_API_KEY=your_context7_key_here
JUPYTER_TOKEN=my_secure_token_123
TRANSCRIPT_API_KEY=your_transcript_key_here

# Other API Keys
ANTHROPIC_API_KEY=your_anthropic_key
```

### Verifying MCP Server Installation

After adding MCP servers, verify they're configured:

```bash
claude mcp list
```

### Removing MCP Servers

To remove a server:

```bash
claude mcp remove <server-name>
```

## Customizing for Your Project

1. **Update CLAUDE.md** with your project-specific instructions
2. **Create custom agents** for specialized tasks in your domain
3. **Add skills** for common workflows you want to reuse
4. **Add commands** for quick shortcuts
5. **Update .env.example** with your project's required environment variables
6. **Modify .gitignore** if you have additional files to ignore

## Best Practices

### Agents
- Create agents for specialized domains or expertise areas
- Include specific tool access in the frontmatter
- Write clear descriptions so Claude knows when to use them
- Keep agent instructions focused on their specialty

### Skills
- Use skills for multi-step workflows that you'll reuse
- Document the workflow clearly with steps
- Include examples in the SKILL.md
- Make skills self-contained

### Commands
- Keep commands simple and focused
- Use commands for quick, common tasks
- Commands should do one thing well

### Environment Variables
- Never commit `.env` to git
- Keep `.env.example` updated with required variables
- Use descriptive variable names
- Document what each variable is for

## Troubleshooting

### Script won't execute
```bash
chmod +x scripts/claude-with-env.sh
```

### Environment variables not loading
- Check that `.env` exists in the project root
- Verify the file path in `claude-with-env.sh`
- Make sure variables are exported (no spaces around `=`)

### Agent/Skill not recognized
- Check the frontmatter syntax
- Verify the file is in the correct directory
- Ensure the name matches what you're invoking

## Examples

This boilerplate includes example templates and production-ready skills:

### Templates
- `.claude/agents/example-agent.md` - Agent template with explanation
- `.claude/skills/example-skill/SKILL.md` - Skill template with workflow
- `.claude/commands/example-command.md` - Command template

### Production Skills
- `.claude/skills/mermaid-diagram-specialist/SKILL.md` - Create flowcharts, sequence diagrams, ERDs, C4 diagrams, and more
  - Use: `/mermaid-diagram-specialist` when creating technical documentation or visualizing architecture
  - Supports: 10+ diagram types including flowcharts, sequence diagrams, ERDs, state diagrams, and Gantt charts

- `.claude/skills/xlsx/SKILL.md` - Excel file creation, editing, and analysis
  - Use: `/xlsx` when working with spreadsheets (.xlsx, .xlsm, .csv, .tsv)
  - Features: Formula management, financial modeling, data analysis, professional formatting

These are fully functional examples you can use as starting points or use directly in your projects.

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/claude/docs)
- [MCP Servers](https://modelcontextprotocol.io/introduction)
- [Creating Custom Agents](https://docs.anthropic.com/claude/docs/agents)

## License

This boilerplate is provided as-is for use with your projects. Customize freely!

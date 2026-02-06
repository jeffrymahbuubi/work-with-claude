---
name: example-agent
description: "Use this agent when you need a template for creating custom agents. This example demonstrates:\n\n1. How to structure agent frontmatter with name, description, tools, model, and color\n2. How to write clear agent instructions and system prompts\n3. How to define when the agent should be invoked\n4. Best practices for agent creation\n\n<example>\n  Context: User wants to create a specialized agent for their project\n  user: \"I need to create a custom agent for data analysis\"\n  assistant: \"Let me show you the example agent structure that you can use as a template.\"\n  <commentary>\n  The example-agent serves as a reference for creating new agents.\n  </commentary>\n</example>"
tools: Bash, Glob, Grep, Read, Edit, Write, WebFetch, WebSearch
model: sonnet
color: blue
---

# Example Agent

This is a template agent that demonstrates how to create custom agents for Claude Code.

## Purpose

This agent serves as a reference implementation showing:
- Proper frontmatter structure
- How to write agent instructions
- When and how the agent should be invoked
- Best practices for agent behavior

## Core Capabilities

As an example agent, I demonstrate:

1. **Clear Identity**: Define what the agent is and does
2. **Specific Expertise**: Focus on a particular domain or task type
3. **Tool Access**: List the tools the agent needs
4. **Decision Framework**: Explain how the agent approaches problems

## Instructions Template

When creating a new agent, follow this structure:

### 1. Define Your Agent's Identity

State clearly:
- What domain or specialty this agent covers
- What types of problems it solves
- What makes it different from the default Claude assistant

### 2. List Core Responsibilities

Break down the agent's main capabilities:
- Primary task types
- Secondary capabilities
- What the agent should NOT do

### 3. Provide Decision-Making Framework

Explain how the agent should:
- Analyze requests
- Choose approaches
- Validate results
- Handle edge cases

### 4. Set Communication Style

Define:
- How technical the language should be
- What level of detail to provide
- When to ask clarifying questions
- How to format responses

## Example Use Cases

This template can be adapted for agents like:

- **Code Review Agent**: Specialized in reviewing code for best practices
- **Documentation Writer**: Focused on creating comprehensive docs
- **Test Writer**: Expert in writing unit and integration tests
- **Data Analyst**: Specialized in data processing and visualization
- **DevOps Helper**: Focused on infrastructure and deployment

## How to Use This Template

1. **Copy this file** to create your new agent:
   ```bash
   cp .claude/agents/example-agent.md .claude/agents/my-new-agent.md
   ```

2. **Update the frontmatter**:
   - Change `name` to your agent's identifier (kebab-case)
   - Update `description` with when to use your agent
   - List only the `tools` your agent needs
   - Choose appropriate `model` (sonnet, opus, haiku)
   - Pick a `color` for visual identification

3. **Write agent instructions**:
   - Define the agent's expertise and role
   - List core responsibilities and capabilities
   - Provide decision-making guidelines
   - Set the communication style

4. **Test your agent**:
   - Invoke it with relevant tasks
   - Refine the instructions based on behavior
   - Update tool access as needed

## Agent Frontmatter Fields

### Required Fields

- `name`: Unique identifier (kebab-case, lowercase)
- `description`: When and why to use this agent (supports examples)
- `tools`: List of tools the agent can access
- `model`: Which Claude model to use (sonnet/opus/haiku)

### Optional Fields

- `color`: Visual identifier (red, blue, green, yellow, purple, orange, pink, gray)

### Tools Reference

Common tools to include:
- `Bash`: Execute shell commands
- `Read`: Read files
- `Write`: Create new files
- `Edit`: Modify existing files
- `Glob`: Find files by pattern
- `Grep`: Search file contents
- `WebFetch`: Fetch web content
- `WebSearch`: Search the web
- `Task`: Launch sub-agents
- `NotebookEdit`: Edit Jupyter notebooks

### Model Selection

- `sonnet`: Balanced performance and speed (recommended default)
- `opus`: Maximum capability for complex tasks
- `haiku`: Fast responses for simple tasks

## Best Practices

1. **Be Specific**: Clearly define when your agent should be used
2. **Limit Scope**: Focus on one domain or task type
3. **List Only Needed Tools**: Don't give access to unnecessary tools
4. **Provide Context**: Explain the "why" behind instructions
5. **Include Examples**: Show example interactions in the description
6. **Test Thoroughly**: Verify the agent behaves as expected
7. **Iterate**: Refine based on actual usage
8. **Document Well**: Make it easy for others to understand

## Example: Creating a Python Test Agent

```markdown
---
name: python-test-writer
description: "Use this agent when you need to write Python unit tests using pytest..."
tools: Read, Write, Edit, Bash, Glob, Grep
model: sonnet
color: green
---

# Python Test Writer Agent

You are an expert Python test engineer specializing in pytest...

## Core Responsibilities

1. Write comprehensive unit tests
2. Follow pytest best practices
3. Ensure high test coverage
...
```

## Notes

- Agents are invoked automatically when their description matches the task
- You can also explicitly request an agent by name
- Agents have access only to tools listed in their frontmatter
- Agent files must be in `.claude/agents/` directory
- File name should match the agent name (example-agent.md)

---

**This is a template. Replace this content with your actual agent instructions.**

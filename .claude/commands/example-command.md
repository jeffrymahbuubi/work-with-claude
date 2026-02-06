---
name: example-command
description: Template demonstrating how to create simple, focused commands for common tasks
---

# Example Command Template

This is a template for creating custom commands in Claude Code. Commands are simple, focused shortcuts for common tasks.

## What is a Command?

Commands are lightweight, single-purpose instructions that tell Claude to perform a specific action. Unlike skills (which are multi-step workflows) or agents (which are specialized AI assistants), commands are simple and direct.

## When to Use Commands

Create commands for:
- Quick, frequently-used tasks
- Simple one-step actions
- Shortcuts for common operations
- Tasks that don't need multi-step workflows

**Examples of good commands:**
- `/format` - Format code in current file
- `/test` - Run project tests
- `/docs` - Generate documentation
- `/clean` - Clean build artifacts
- `/deploy` - Deploy to production

## Command Structure

Commands consist of:
1. **Frontmatter** - Metadata (name, description)
2. **Instructions** - What Claude should do

```markdown
---
name: command-name
description: Brief description of what this command does
---

# Command Instructions

When this command is invoked, Claude should:

1. [First action]
2. [Second action]
3. [Final action]

[Any additional context or requirements]
```

## Creating Your Own Command

### 1. Choose a Command Name

- Use lowercase, single words or hyphenated phrases
- Make it memorable and intuitive
- Keep it short (1-2 words)

**Good names:**
- `test`, `build`, `deploy`, `format`
- `check-types`, `run-linter`, `update-deps`

**Bad names:**
- `do-the-thing-that-formats-and-lints` (too long)
- `x`, `cmd1` (not descriptive)

### 2. Write Clear Instructions

Be specific about what Claude should do:

```markdown
When this command is invoked:

1. Run the test suite using pytest
2. Generate a coverage report
3. Display the summary
4. If tests fail, show the error details
```

### 3. Add the Command File

Save as `.claude/commands/your-command-name.md`

### 4. Test It

Invoke with `/your-command-name` in conversation

## Example Commands

### Example 1: Format Command

```markdown
---
name: format
description: Format all code files in the project using the project's formatter
---

# Format Command

When this command is invoked:

1. Identify the project type (Python, JavaScript, etc.)
2. Use the appropriate formatter:
   - Python: Run `black .` and `isort .`
   - JavaScript/TypeScript: Run `prettier --write .`
   - Other: Ask which formatter to use
3. Show which files were formatted
4. Report any formatting errors
```

### Example 2: Test Command

```markdown
---
name: test
description: Run the project's test suite and display results
---

# Test Command

When this command is invoked:

1. Detect the test framework (pytest, jest, etc.)
2. Run the appropriate test command
3. Display test results summary
4. If tests fail, show failure details
5. If available, show coverage information
```

### Example 3: Clean Command

```markdown
---
name: clean
description: Remove build artifacts, cache files, and temporary files
---

# Clean Command

When this command is invoked:

1. Remove common build artifacts:
   - `dist/`, `build/`, `*.egg-info/`
   - `node_modules/` (if user confirms)
   - `__pycache__/`, `*.pyc`
   - `.pytest_cache/`
2. List what was removed
3. Report disk space freed
```

### Example 4: Deploy Command

```markdown
---
name: deploy
description: Deploy the application to production
---

# Deploy Command

When this command is invoked:

1. **Safety check**: Ask user to confirm production deployment
2. Run pre-deployment checks:
   - Ensure tests pass
   - Check for uncommitted changes
   - Verify on correct branch
3. Build production artifacts
4. Deploy using project's deployment method
5. Report deployment status and URL
```

### Example 5: Docs Command

```markdown
---
name: docs
description: Generate or update project documentation
---

# Docs Command

When this command is invoked:

1. Identify documentation system (Sphinx, JSDoc, etc.)
2. Generate documentation from code
3. Update README if needed
4. Generate API documentation
5. Report what was generated and where
```

## Best Practices

### Keep Commands Simple

- One clear purpose per command
- No complex decision trees
- If it needs multiple steps, consider a skill instead

### Make Commands Safe

- Ask for confirmation before destructive actions
- Validate prerequisites before execution
- Provide clear error messages

### Provide Good Feedback

- Show what's happening
- Report success or failure clearly
- Suggest next steps

### Be Consistent

- Use similar naming patterns
- Follow project conventions
- Document behavior clearly

## Commands vs Skills vs Agents

### Use a Command when:
- Task is simple and direct
- One or two steps maximum
- Frequently used shortcut
- No complex decision-making

### Use a Skill when:
- Multi-step workflow
- Needs validation checkpoints
- Reusable process
- Multiple related tasks

### Use an Agent when:
- Specialized expertise needed
- Complex problem-solving
- Domain-specific knowledge
- Multiple tool interactions

## Testing Your Command

1. **Invoke the command**
   ```
   /your-command-name
   ```

2. **Verify behavior**
   - Does it do what you expect?
   - Are error messages helpful?
   - Is output clear?

3. **Test edge cases**
   - What if prerequisites are missing?
   - How does it handle errors?
   - What if files don't exist?

4. **Refine**
   - Update instructions based on testing
   - Clarify ambiguous steps
   - Add error handling notes

## Common Patterns

### File Operation Pattern
```markdown
1. Check file exists
2. Read/modify file
3. Write changes
4. Report what changed
```

### Build Pattern
```markdown
1. Clean previous build
2. Run build command
3. Verify build succeeded
4. Report output location
```

### Check Pattern
```markdown
1. Run validation/check
2. Parse results
3. Report pass/fail
4. Show errors if any
```

### Update Pattern
```markdown
1. Check current version
2. Fetch updates
3. Apply changes
4. Verify success
```

## Customization Tips

1. **Add parameters**: Commands can accept arguments
   ```
   /deploy staging
   /test unit
   ```

2. **Environment-specific**: Tailor to your project
   ```markdown
   For this project, use:
   - npm run test (not jest directly)
   - python manage.py runserver (Django)
   ```

3. **Project conventions**: Follow your team's practices
   ```markdown
   Follow the commit message format:
   [type]: description
   ```

## Notes

- Commands are invoked with `/command-name`
- Keep command files in `.claude/commands/`
- File name should match command name
- Commands should be quick to execute
- For complex tasks, use skills or agents instead
- Test commands before relying on them
- Document any special requirements

---

**This is a template. Replace with your actual command instructions.**

## Quick Start Template

```markdown
---
name: your-command
description: What your command does
---

# Your Command

When this command is invoked:

1. [First action]
2. [Second action]
3. [Report results]

[Any special notes or requirements]
```

Copy this template to create new commands!

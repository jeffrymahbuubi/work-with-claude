# UV Python Project Setup Guide

**Best Practices for Modern Python Projects with UV**

---

## Overview

This guide provides best practices for setting up Python projects using UV, a modern Python package manager that offers faster dependency resolution and better project management than traditional tools.

**Key Benefits of UV:**
- ⚡ **Fast**: 10-100x faster than pip
- 🔒 **Reproducible**: Lock files ensure consistent builds
- 📦 **Modern**: Uses `pyproject.toml` standard (PEP 621)
- 🎯 **Simple**: Single tool for virtual environments and packages
- 🔄 **Compatible**: Works with existing pip/poetry projects

---

## Why Use pyproject.toml?

### Old Approach: `requirements.txt` Only

```bash
# Manual workflow - error-prone
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# To add package:
echo "new-package>=1.0.0" >> requirements.txt
pip install -r requirements.txt
```

**Problems:**
- ❌ No metadata about Python version requirements
- ❌ No project metadata (name, version, description)
- ❌ Manual dependency management (editing text files)
- ❌ No lock file for reproducible builds
- ❌ Python version conflicts discovered late (at install time)
- ❌ Can't use modern `uv add`/`uv remove` commands

### Modern Approach: `pyproject.toml` + UV

```bash
# Automated workflow - robust
uv init
uv python pin 3.11
uv add new-package  # Automatically updates pyproject.toml
uv sync             # Installs everything consistently
```

**Benefits:**
- ✅ **Python version enforcement** - `requires-python` prevents incompatible versions
- ✅ **Centralized metadata** - Project name, version, description in one place
- ✅ **Automated dependency management** - `uv add`/`uv remove` handle everything
- ✅ **Lock file** - `uv.lock` ensures reproducible builds across machines
- ✅ **Early conflict detection** - UV resolves dependencies before installation
- ✅ **Standard format** - PEP 621 compliant, works with all modern Python tools
- ✅ **Editable installs** - `uv sync` automatically installs your project in dev mode

---

## Quick Start: Create a New Project

```bash
# Start ANY new Python project with these commands:
mkdir my-project && cd my-project
uv init --no-workspace
uv python pin 3.11
uv add your-dependencies
echo ".venv/" >> .gitignore
git init && git add . && git commit -m "Initial commit"
uv run python main.py
```

---

## Step-by-Step: Proper UV Project Setup

### 1. Initialize Project with pyproject.toml

```bash
cd your-project/
uv init --no-workspace
```

This creates:
- `pyproject.toml` - Project metadata and dependencies
- `.python-version` - Pinned Python version
- `README.md` - Basic documentation

### 2. Pin Python Version

```bash
# Pin to specific Python version (if package has specific requirements)
uv python pin 3.11
```

This creates `.python-version` file:
```
3.11
```

### 3. Add Dependencies

```bash
# Add packages using uv add (not manual requirements.txt editing)
uv add numpy pandas matplotlib
uv add cisco-ai-mcp-scanner cisco-ai-skill-scanner
```

This updates `pyproject.toml`:
```toml
[project]
name = "your-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "cisco-ai-mcp-scanner>=1.0.1",
    "cisco-ai-skill-scanner>=1.0.2",
    "matplotlib>=3.10.8",
    "numpy>=2.2.6",
    "pandas>=2.3.3",
]
```

### 4. Sync Environment

```bash
# Install all dependencies from lock file
uv sync
```

This creates:
- `.venv/` - Virtual environment with correct Python version
- `uv.lock` - Deterministic dependency resolution (like package-lock.json)

### 5. Run Your Code

```bash
# Run scripts with project's Python + dependencies
uv run python your_script.py
uv run pytest
```

---

## Common UV Commands Reference

### Project Setup
```bash
uv init                      # Create new project with pyproject.toml
uv init --no-workspace       # Single project (not part of workspace)
uv python pin 3.11           # Pin Python version in .python-version
```

### Dependency Management
```bash
uv add package-name          # Add dependency to pyproject.toml
uv add --dev pytest          # Add dev dependency
uv remove package-name       # Remove dependency
uv sync                      # Install all dependencies from lock file
uv sync --upgrade            # Upgrade all dependencies
uv lock                      # Update lock file without installing
```

### Running Code
```bash
uv run python script.py      # Run with project's Python + dependencies
uv run pytest                # Run tests with project environment
uv run --python 3.12 script  # Override Python version temporarily
```

### Environment Management
```bash
uv venv                      # Create .venv (usually automatic)
uv pip list                  # List installed packages
uv pip install -e .          # Install project in editable mode
```

---

## Migration Guide: requirements.txt → pyproject.toml

If you have an existing project with `requirements.txt`:

```bash
# 1. Initialize UV project (migrates requirements.txt automatically)
cd your-project/
uv init --no-workspace

# 2. Update Python version if needed
uv python pin 3.11

# 3. Sync to create new venv with correct Python version
uv sync

# 4. Verify everything works
uv run python your_script.py

# 5. (Optional) Keep requirements.txt for backwards compatibility
# UV will keep it in sync with pyproject.toml
```

**What `uv init` does:**
- Creates `pyproject.toml` from existing `requirements.txt`
- Detects current Python version from `.venv` or system
- Preserves all your dependencies with version constraints
- Does NOT delete `requirements.txt` (you can keep both)

---

## Best Practices for New Python Projects

### ✅ DO: Start with UV Init

```bash
# Good: Modern workflow from the start
mkdir my-project && cd my-project
uv init
uv python pin 3.11
uv add numpy pandas matplotlib
uv run python main.py
```

### ❌ DON'T: Manual venv + requirements.txt

```bash
# Bad: Old workflow, will cause problems later
mkdir my-project && cd my-project
python -m venv .venv
echo "numpy" > requirements.txt
pip install -r requirements.txt
```

---

## Project Structure Recommendation

```
my-project/
├── pyproject.toml          # ✅ Project metadata + dependencies
├── uv.lock                 # ✅ Lock file (committed to git)
├── .python-version         # ✅ Python version pin
├── requirements.txt        # ⚠️  Optional, for backwards compatibility
├── .venv/                  # ❌ Never commit (add to .gitignore)
├── src/
│   └── my_project/
│       └── __init__.py
├── tests/
│   └── test_main.py
└── scripts/
    └── scan_tools.py
```

**`.gitignore` entries:**
```gitignore
.venv/
__pycache__/
*.pyc
.pytest_cache/
*.egg-info/
```

**Commit to git:**
```bash
git add pyproject.toml uv.lock .python-version
git commit -m "Initialize project with UV"
```

---

## Troubleshooting Common Issues

### Issue 1: Python Version Conflict

**Error:**
```
error: The Python request from `.python-version` resolved to Python 3.10.12,
which is incompatible with the project's Python requirement: `>=3.11`
```

**Solution:**
```bash
uv python pin 3.11   # Update .python-version
uv sync              # Recreate venv with correct Python
```

### Issue 2: Package Requires Newer Python

**Error:**
```
Because package-name depends on Python>=3.11 and current Python is 3.10
```

**Solution:**
```bash
# Update Python version in pyproject.toml
uv python pin 3.11
uv sync
```

Or edit `pyproject.toml`:
```toml
requires-python = ">=3.11"  # Update this line
```

### Issue 3: No pyproject.toml Found

**Error:**
```
error: No `pyproject.toml` found in current directory
```

**Solution:**
```bash
# Initialize project first
uv init --no-workspace
uv add your-package
```

### Issue 4: Conflicting Dependencies

**Error:**
```
× No solution found when resolving dependencies
```

**Solution:**
```bash
# Check what's conflicting
uv tree

# Try upgrading all dependencies
uv sync --upgrade

# Or pin specific versions in pyproject.toml
```

---

## When to Use requirements.txt vs pyproject.toml

### Use `pyproject.toml` (Preferred)

**For:**
- ✅ New projects (always)
- ✅ Applications you develop and deploy
- ✅ Libraries you publish to PyPI
- ✅ Projects with multiple contributors
- ✅ CI/CD pipelines (reproducible builds)

**Why:**
- Modern standard (PEP 621)
- Better dependency resolution
- Lock file support
- Python version enforcement

### Keep `requirements.txt` (Optional)

**For:**
- ⚠️  Legacy compatibility (Docker images, old CI)
- ⚠️  Simple scripts shared with non-UV users
- ⚠️  Documentation/examples

**How to maintain both:**
```bash
# UV can export to requirements.txt
uv pip compile pyproject.toml -o requirements.txt

# Or just keep both - UV updates requirements.txt automatically
```

---

## Summary: Key Takeaways

1. **Always start with `uv init`** - Don't create manual venvs
2. **Pin Python version early** - Use `uv python pin X.Y` before adding packages
3. **Use `uv add` for dependencies** - Don't edit `pyproject.toml` manually
4. **Commit lock files** - `uv.lock` ensures team consistency
5. **Modern tooling = fewer problems** - Let UV handle dependency resolution

---

## Additional Resources

- **UV Documentation:** https://docs.astral.sh/uv/
- **PEP 621 (pyproject.toml):** https://peps.python.org/pep-0621/
- **UV vs pip/poetry comparison:** https://docs.astral.sh/uv/pip/compatibility/

---

**Best Practice:** Use UV for all new Python projects. It's faster, more reliable, and follows modern Python standards.

# Claude Skills Security Scanner

A comprehensive Python script that uses [cisco-ai-skill-scanner](https://github.com/cisco-ai-defense/skill-scanner) to scan Claude Code skills for security vulnerabilities.

**Repository:** https://github.com/cisco-ai-defense/skill-scanner
**PyPI Package:** cisco-ai-skill-scanner
**License:** Apache 2.0

---

## Overview

The **cisco-ai-skill-scanner** is a comprehensive security scanner for AI Agent Skills that combines multiple detection engines to identify security vulnerabilities in Claude Code skills, OpenAI Codex Skills, and Cursor Agent Skills.

This script provides a wrapper around the library with enhanced reporting, CI/CD integration, and multi-analyzer orchestration.

---

## Features

### 🔍 Multi-Engine Detection

The scanner uses **6 different analysis engines** that can be combined for comprehensive threat detection:

| Engine | Type | Scope | Requires API Key | Description |
|--------|------|-------|------------------|-------------|
| **Static** | Pattern-based | All files | ❌ No | YAML + YARA patterns for known malicious patterns |
| **Behavioral** | Dataflow analysis | Python files | ❌ No | AST-based taint tracking and dataflow analysis |
| **LLM** | Semantic AI | SKILL.md + scripts | ✅ Yes | Claude API for semantic understanding |
| **Meta** | False positive filtering | All findings | ✅ Yes | AI-powered FP reduction and prioritization |
| **VirusTotal** | Hash-based | Binary files | ✅ Yes | Malware detection for binaries |
| **AI Defense** | Cloud-based AI | Text content | ✅ Yes | Cisco AI Defense cloud scanning |

### 🎯 Threat Detection Capabilities

The scanner can detect:

#### Critical Threats
- **Prompt Injection Attacks** - Malicious instructions hidden in skill definitions
- **Data Exfiltration** - Reading sensitive files and transmitting to external servers
- **Command Injection** - Unsafe execution of system commands
- **Credential Theft** - Accessing AWS credentials, SSH keys, API tokens
- **Malicious Code Execution** - Use of `eval()`, `exec()`, `pickle.loads()`

#### Security Patterns
- **Network Operations** - HTTP requests to external URLs
- **File System Access** - Reading/writing sensitive files
- **Environment Variables** - Accessing secrets from env vars
- **Obfuscated Code** - Base64 encoding, unicode tricks, hex encoding
- **Dangerous Functions** - Known risky Python/JavaScript functions

#### Policy Violations
- Missing license information
- Missing author information
- Unclear skill descriptions
- Overly broad permissions

### 📊 Output Formats

The scanner supports multiple output formats for different use cases:

| Format | Use Case | File Extension |
|--------|----------|----------------|
| **Summary** | Quick console overview | Terminal output |
| **JSON** | CI/CD integration, automation | `.json` |
| **Markdown** | Human-readable reports | `.md` |
| **Table** | Terminal-friendly comparison | Terminal output |
| **SARIF** | GitHub Code Scanning integration | `.sarif` |

### 🔧 Detection Modes

The scanner offers three detection sensitivity levels:

- **Strict Mode** - Maximum sensitivity, higher false positive rate
- **Balanced Mode** (default) - Good balance of detection and precision
- **Permissive Mode** - Fewer findings, may miss some threats

---

## Installation

Install the `cisco-ai-skill-scanner` package in your Python environment:

```bash
# Using pip
pip install cisco-ai-skill-scanner

# Using uv
uv pip install cisco-ai-skill-scanner

# Verify installation
pip list | grep skill
```

---

## Usage

### Basic Scan (Static Analyzer Only)

```bash
python scripts/python/scan_claude_skills.py --skills-dir .claude/skills
```

### Scan with Behavioral Analysis

```bash
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --use-behavioral
```

### Generate Reports

```bash
# JSON report only
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --format json \
  --output skill_scan_report.json

# Markdown report only
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --format markdown \
  --output skill_scan_report.md

# Both JSON and Markdown
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --format both \
  --output skill_scan_report
```

### CI/CD Mode (Fail on High/Critical Findings)

```bash
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --use-behavioral \
  --fail-on-findings
# Exit code: 0 if safe, 1 if critical/high findings detected
```

### With LLM Analyzer (Optional)

```bash
# Set API key first
export SKILL_SCANNER_LLM_API_KEY="your_anthropic_api_key"
export SKILL_SCANNER_LLM_MODEL="claude-3-5-sonnet-20241022"

# Run scan with LLM analyzer
python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --use-behavioral \
  --use-llm
```

---

## Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--skills-dir` | Path to Claude skills directory | `.claude/skills` |
| `--use-behavioral` | Enable behavioral analyzer (dataflow analysis) | `False` |
| `--use-llm` | Enable LLM analyzer (requires API key) | `False` |
| `--format` | Output format: `summary`, `json`, `markdown`, `both` | `summary` |
| `--output` | Output file path | Auto-generated timestamp |
| `--fail-on-findings` | Exit code 1 if HIGH/CRITICAL found | `False` |
| `--recursive` | Scan skills recursively | `True` |

---

## Example Output

### Console Summary

```
================================================================================
   Claude Skills Security Scanner
   Powered by Cisco AI Defense Skill Scanner
================================================================================

📁 Skills Directory: /path/to/.claude/skills
🔍 Recursive Scan: True
🔬 Analyzers: Static (YAML+YARA), Behavioral (Dataflow)

🚀 Starting scan...

================================================================================
SCAN RESULTS
================================================================================
Total Skills Scanned: 2
Safe Skills: 2 ✅
Unsafe Skills: 0 ⚠️
Total Findings: 1

Severity Breakdown:
  ⚪ INFO: 1

================================================================================
DETAILED FINDINGS
================================================================================

📦 Skill: mermaid-diagram-specialist - ✅ SAFE
   Max Severity: ⚪ INFO
   Total Findings: 1

  ⚪ INFO Findings (1):
  ----------------------------------------------------------------------------

    [INFO] Skill does not specify a license
    Rule: MANIFEST_MISSING_LICENSE
    Description: Skill manifest does not include a 'license' field.
    Location: SKILL.md
```

### Severity Levels

| Emoji | Severity | Description |
|-------|----------|-------------|
| 🔴 | CRITICAL | Immediate security threat |
| 🟠 | HIGH | Serious vulnerability |
| 🟡 | MEDIUM | Moderate risk |
| 🔵 | LOW | Minor issue |
| ⚪ | INFO | Informational |
| ✅ | SAFE | No issues found |

---

## Architecture

### How It Works

```
┌─────────────────────────────────────────────────────────────┐
│                      Skill Directory                         │
│  (.claude/skills/my-skill/)                                  │
│                                                              │
│  ├── SKILL.md          (Skill definition)                   │
│  ├── scripts/          (Python/JS/Bash scripts)             │
│  └── manifest.yaml     (Metadata)                           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    SkillScanner                              │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Static     │  │  Behavioral  │  │     LLM      │      │
│  │  Analyzer    │  │   Analyzer   │  │   Analyzer   │      │
│  │              │  │              │  │              │      │
│  │ YAML+YARA    │  │ AST Dataflow │  │ Claude API   │      │
│  │  Patterns    │  │   Analysis   │  │   Semantic   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│          │                 │                  │              │
│          └─────────────────┴──────────────────┘              │
│                            │                                 │
│                            ▼                                 │
│  ┌──────────────────────────────────────────────────┐      │
│  │          Finding Aggregation                      │      │
│  │  - Deduplicate findings                          │      │
│  │  - Calculate severity                            │      │
│  │  - Group by category                             │      │
│  └──────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Report Generation                          │
│                                                              │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐  ┌─────────┐ │
│  │   JSON    │  │ Markdown  │  │  SARIF    │  │  Table  │ │
│  └───────────┘  └───────────┘  └───────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## Understanding the Analyzers

### 1. Static Analyzer (Always Enabled)

Uses YAML + YARA pattern matching to detect:
- Dangerous function calls (`eval`, `exec`, `pickle.loads`)
- Network operations to external URLs
- File system access patterns
- Environment variable access
- Base64 encoding patterns
- Obfuscated code
- Policy violations

### 2. Behavioral Analyzer (Optional: `--use-behavioral`)

Performs AST-based dataflow analysis to detect:
- Data exfiltration (reading files + network transmission)
- Taint tracking from user inputs to dangerous sinks
- Command injection chains
- Credential theft patterns
- Cross-file data flow

### 3. LLM Analyzer (Optional: `--use-llm`)

Uses Claude API for semantic understanding:
- Intent analysis of SKILL.md instructions
- Detection of subtle malicious patterns
- Context-aware threat assessment
- False positive reduction via meta-analysis

---

## Performance

### Scan Speed

| Skill Size | Static Only | + Behavioral | + LLM |
|------------|-------------|--------------|-------|
| Small (< 5 files) | < 1 sec | 1-2 sec | 3-5 sec |
| Medium (5-20 files) | 1-2 sec | 2-5 sec | 5-10 sec |
| Large (> 20 files) | 2-5 sec | 5-15 sec | 10-30 sec |

---

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Skill Security Scan

on:
  push:
    paths:
      - '.claude/skills/**'
  pull_request:

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Dependencies
        run: |
          pip install cisco-ai-skill-scanner

      - name: Scan Skills
        run: |
          python scripts/python/scan_claude_skills.py \
            --skills-dir .claude/skills \
            --use-behavioral \
            --format sarif \
            --output results.sarif \
            --fail-on-findings

      - name: Upload SARIF
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: results.sarif
```

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

python scripts/python/scan_claude_skills.py \
  --skills-dir .claude/skills \
  --use-behavioral \
  --fail-on-findings

if [ $? -ne 0 ]; then
  echo "❌ Skill security scan failed. Fix issues before committing."
  exit 1
fi
```

---

## Troubleshooting

### ModuleNotFoundError: No module named 'skill_scanner'

**Solution:** Install the package:

```bash
pip install cisco-ai-skill-scanner
# or
uv pip install cisco-ai-skill-scanner
```

### LLM Analyzer Not Working

**Solution:** Set the required environment variables:

```bash
export SKILL_SCANNER_LLM_API_KEY="your_api_key"
export SKILL_SCANNER_LLM_MODEL="claude-3-5-sonnet-20241022"
```

### Permission Denied

**Solution:** Make script executable:

```bash
chmod +x scripts/python/scan_claude_skills.py
```

---

## Next Steps

### Recommended Workflow

1. **Initial Scan**
   ```bash
   # Quick scan with static analyzer
   python scripts/python/scan_claude_skills.py --skills-dir .claude/skills
   ```

2. **Deep Analysis**
   ```bash
   # Add behavioral analysis
   python scripts/python/scan_claude_skills.py \
     --skills-dir .claude/skills \
     --use-behavioral \
     --format both \
     --output deep_scan
   ```

3. **CI/CD Integration**
   - Add pre-commit hook
   - Set up GitHub Actions
   - Enable SARIF upload for Code Scanning

4. **Regular Scans**
   - Scan before installing new skills
   - Re-scan after skill updates
   - Monthly security audits

---

## References

- **GitHub:** https://github.com/cisco-ai-defense/skill-scanner
- **PyPI:** https://pypi.org/project/cisco-ai-skill-scanner/
- **Discord:** https://discord.com/invite/nKWtDcXxtx
- **Documentation:** https://github.com/cisco-ai-defense/skill-scanner/tree/main/docs
- **Cisco AI Defense:** https://www.cisco.com/site/us/en/products/security/ai-defense/
- **Threat Taxonomy:** https://github.com/cisco-ai-defense/skill-scanner/blob/main/docs/threat-taxonomy.md

---

**Script Location**: `scripts/python/scan_claude_skills.py`
**License:** Apache 2.0

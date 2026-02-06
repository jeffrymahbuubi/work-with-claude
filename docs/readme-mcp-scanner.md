# MCP Scanner Security Tool

## Overview

The **MCP Scanner** is a comprehensive security analysis tool developed by Cisco AI Defense for scanning Model Context Protocol (MCP) servers and tools for potential security vulnerabilities. It combines multiple detection engines to identify threats in MCP configurations, tools, prompts, resources, and server instructions.

Repository: [cisco-ai-defense/mcp-scanner](https://github.com/cisco-ai-defense/mcp-scanner)

## Key Features

### Multi-Engine Security Analysis

The MCP Scanner provides three powerful scanning engines that can be used independently or together:

#### 1. **YARA Analyzer** (No API Key Required)
- Pattern-based threat detection using YARA rules
- Detects suspicious code patterns, command injection risks, file access violations
- Fast, offline scanning capability
- Ideal for CI/CD pipelines and air-gapped environments
- **Recommended for initial scans**

#### 2. **LLM Analyzer** (Requires LLM API Key)
- Semantic analysis using large language models
- LLM-as-a-judge approach for detecting:
  - Prompt injection attacks
  - Tool poisoning
  - Misleading documentation
  - Behavioral anomalies
- Supports multiple LLM providers:
  - OpenAI GPT-4o/4.1
  - AWS Bedrock Claude 4.5 Sonnet
  - Azure OpenAI
  - Local LLMs (Ollama, vLLM, LocalAI)

#### 3. **API Analyzer** (Requires Cisco AI Defense API Key)
- Integration with Cisco AI Defense Inspect API
- Advanced threat detection and classification
- Cloud-based analysis with updated threat intelligence

### Comprehensive Scanning Capabilities

The scanner can analyze:

- **MCP Tools**: Scan tool definitions for security risks
- **MCP Prompts**: Detect prompt injection and manipulation risks
- **MCP Resources**: Analyze resource access patterns
- **Server Instructions**: Check initialization and configuration for security issues
- **Source Code**: Behavioral analysis of MCP server implementation
- **Static/Offline Files**: Scan pre-generated JSON files without live connections

### Multiple Scanning Modes

1. **Stdio Servers**: Scan local MCP servers launched via command-line
2. **HTTP/SSE Servers**: Scan remote MCP servers via HTTP endpoints
3. **Config File Scanning**: Scan all servers defined in MCP configuration files
4. **Well-Known Configs**: Auto-discover and scan servers from standard locations
5. **Static/Offline Mode**: CI/CD-friendly scanning of JSON artifacts

## Installation

Install the MCP Scanner in your Python environment:

```bash
# Using pip
pip install cisco-ai-mcp-scanner

# Using uv
uv pip install cisco-ai-mcp-scanner

# Verify installation
pip show cisco-ai-mcp-scanner
```

## Security Threats Detected

The MCP Scanner uses the **AITech Threat Taxonomy** to classify security findings:

### High Severity Threats

- **Command Injection**: Execution of arbitrary system commands
- **Path Traversal**: Unauthorized file system access
- **Prompt Injection**: Manipulation of LLM behavior through prompts
- **Tool Poisoning**: Malicious tool definitions or behaviors
- **Data Exfiltration**: Unauthorized data extraction
- **Credential Exposure**: Hardcoded secrets or API keys

### Medium Severity Threats

- **Information Disclosure**: Unintended information leakage
- **Insufficient Input Validation**: Missing or weak input sanitization
- **Insecure Defaults**: Unsafe default configurations
- **Missing Authentication**: Lack of proper access controls

### Low Severity Threats

- **Verbose Error Messages**: Information leakage through errors
- **Missing Rate Limiting**: Potential for abuse
- **Weak Encryption**: Use of outdated cryptographic methods

## Using the Scanner

### Quick Start with CLI

The `mcp-scanner` command-line tool provides the fastest way to scan your servers:

```bash
# Scan your MCP config file with YARA (no API key needed)
mcp-scanner config \
  --config-path .mcp.json \
  --analyzers yara \
  --format detailed
```

### Using the Custom Python Script

The included Python script at `scripts/python/scan_mcp_servers.py` provides a comprehensive wrapper.

#### Basic Usage (YARA Only)

```bash
# Scan with default settings (YARA analyzer, default config path)
python scripts/python/scan_mcp_servers.py
```

#### Advanced Usage (Multiple Analyzers)

```bash
# Scan with YARA and LLM analyzers
export MCP_SCANNER_LLM_API_KEY="your_openai_api_key"
python scripts/python/scan_mcp_servers.py --analyzers yara,llm

# Scan with all analyzers
export MCP_SCANNER_API_KEY="your_cisco_api_key"
export MCP_SCANNER_LLM_API_KEY="your_llm_api_key"
python scripts/python/scan_mcp_servers.py --analyzers yara,llm,api
```

#### Custom Config and Output

```bash
# Scan custom config and save to specific location
python scripts/python/scan_mcp_servers.py \
  --config /path/to/custom/.mcp.json \
  --analyzers yara \
  --output /path/to/results.json
```

#### Command-Line Options

```
--config PATH          Path to MCP configuration file (default: .mcp.json in project root)
--analyzers LIST       Comma-separated analyzers: yara, llm, api (default: yara)
--output PATH          Path to save JSON results (default: mcp_scan_results.json)
--api-key KEY          Cisco AI Defense API key (for API analyzer)
--llm-api-key KEY      LLM provider API key (for LLM analyzer)
```

## Understanding Scan Results

### Console Output

The script provides real-time feedback:

```
================================================================================
🔒 MCP SERVER SECURITY SCANNER
================================================================================

Configuration: /path/to/.mcp.json
Analyzers: yara
Servers to scan: 6
================================================================================

📡 Scanning stdio server: fetch
   Command: uvx
   Args: ['mcp-server-fetch']
   ✅ Scanned 3 tools
      Safe: 2, Unsafe: 1

================================================================================
📊 SCAN SUMMARY
================================================================================

Servers:
  Total:    6
  Scanned:  5
  Failed:   1

Tools:
  Total:    45
  ✅ Safe:    38
  ⚠️  Unsafe:  7

Findings:
  Total security findings: 14
```

### JSON Output

Results are saved in a structured JSON format with server details, tool analysis, findings, and summary statistics.

## Security Recommendations

### 1. Regular Scanning

Run security scans:
- **Before deployment**: Scan new MCP servers before adding them to production
- **Weekly**: Automated scans of your MCP configuration
- **After updates**: Scan when MCP server packages are updated
- **CI/CD integration**: Add scanning to your continuous integration pipeline

### 2. Analyzer Selection

- **Development**: Use YARA for fast feedback
- **Pre-production**: Use YARA + LLM for comprehensive analysis
- **Production**: Use all three analyzers for maximum coverage

### 3. Addressing Findings

When the scanner reports unsafe tools:

1. **Review the findings**: Understand what triggered the detection
2. **Check tool documentation**: Verify if the behavior is intentional
3. **Update or replace**: Update to newer versions or find safer alternatives
4. **Request whitelisting**: For known-safe patterns, consider custom YARA rules
5. **Monitor closely**: If a risk must be accepted, implement additional monitoring

### 4. Secure Configuration

- **Remove unused servers**: Disable MCP servers you don't actively use
- **Limit file system access**: Restrict filesystem server to specific directories
- **Rotate credentials**: Regularly update API tokens and bearer tokens
- **Use environment variables**: Don't hardcode sensitive values in config files
- **Enable authentication**: Use OAuth or bearer tokens for remote servers

### 5. Bearer Token Security

If your MCP config has bearer tokens:

```json
{
  "headers": {
    "Authorization": "Bearer sk_YOUR_API_KEY_HERE"
  }
}
```

**Recommendations**:
- Move this token to an environment variable
- Add `.mcp.json` to `.gitignore` if not already present
- Rotate the token if this file has been committed to version control
- Use token expiration/rotation policies

Example secure configuration:
```json
{
  "my-api-server": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${MY_API_TOKEN}"
    }
  }
}
```

## Additional Resources

### Official Documentation

- [MCP Scanner GitHub](https://github.com/cisco-ai-defense/mcp-scanner)
- [Architecture Guide](https://github.com/cisco-ai-defense/mcp-scanner/tree/main/docs/architecture.md)
- [MCP Threats Taxonomy](https://github.com/cisco-ai-defense/mcp-scanner/tree/main/docs/mcp-threats-taxonomy.md)
- [LLM Providers Configuration](https://github.com/cisco-ai-defense/mcp-scanner/tree/main/docs/llm-providers.md)
- [API Reference](https://github.com/cisco-ai-defense/mcp-scanner/tree/main/docs/api-reference.md)

### Cisco AI Defense

- [Cisco AI Defense Product Page](https://www.cisco.com/site/us/en/products/security/ai-defense/index.html)
- [AI Security and Safety Framework](https://learn-cloudsecurity.cisco.com/ai-security-framework)

### Community

- [Discord Server](https://discord.com/invite/nKWtDcXxtx) - Join the community for support and discussions

## Troubleshooting

### Common Issues

#### 1. Server Connection Failures

**Symptom**: `❌ Scan failed: Connection refused` or timeout errors

**Solutions**:
- For stdio servers: Ensure the command is available in PATH
- For HTTP servers: Verify the server is running and accessible
- Check network connectivity and firewall rules
- Verify authentication tokens are valid

#### 2. Missing Dependencies

**Symptom**: `ModuleNotFoundError: No module named 'mcpscanner'`

**Solution**:
```bash
pip install cisco-ai-mcp-scanner
# or
uv pip install cisco-ai-mcp-scanner
```

#### 3. LLM Analyzer Errors

**Symptom**: `LLM analyzer failed: API key not configured`

**Solution**:
```bash
# For OpenAI
export MCP_SCANNER_LLM_API_KEY="sk-..."
export MCP_SCANNER_LLM_MODEL="gpt-4o"

# For AWS Bedrock
export AWS_PROFILE="your-profile"
export AWS_REGION="us-east-1"
export MCP_SCANNER_LLM_MODEL="bedrock/anthropic.claude-sonnet-4-5-20250929-v2:0"
```

### Getting Help

1. **Check the logs**: Review the detailed error messages in the console output
2. **Inspect JSON results**: The scan results JSON file contains detailed error information
3. **GitHub Issues**: Report bugs at [mcp-scanner/issues](https://github.com/cisco-ai-defense/mcp-scanner/issues)
4. **Discord Community**: Ask questions in the Discord server
5. **Documentation**: Review the official docs linked above

## Example Workflow

Here's a complete security scanning workflow:

```bash
#!/bin/bash
# MCP Security Scan Workflow

# 1. Set up environment
export SCAN_DATE=$(date +%Y%m%d)
export RESULTS_DIR="scan_results_${SCAN_DATE}"
mkdir -p "${RESULTS_DIR}"

# 2. Run YARA scan (fast, no API key needed)
echo "Running YARA scan..."
python scripts/python/scan_mcp_servers.py \
  --analyzers yara \
  --output "${RESULTS_DIR}/yara_results.json"

# 3. If critical issues found, run LLM scan for deeper analysis
if grep -q '"unsafe_tools": [1-9]' "${RESULTS_DIR}/yara_results.json"; then
  echo "Unsafe tools detected. Running LLM analysis..."

  # Configure LLM (example with OpenAI)
  export MCP_SCANNER_LLM_API_KEY="${OPENAI_API_KEY}"

  python scripts/python/scan_mcp_servers.py \
    --analyzers llm \
    --output "${RESULTS_DIR}/llm_results.json"
fi

# 4. Generate summary report
echo "Scan complete. Results in ${RESULTS_DIR}/"
ls -lh "${RESULTS_DIR}/"
```

## Conclusion

The MCP Scanner is a powerful tool for ensuring the security of your MCP infrastructure. By integrating security scanning into your development workflow, you can:

- **Detect threats early**: Find security issues before they reach production
- **Maintain compliance**: Document security posture with detailed scan reports
- **Reduce risk**: Identify and remediate vulnerabilities proactively
- **Build confidence**: Deploy MCP servers knowing they've been thoroughly analyzed

Start with YARA-based scanning for quick feedback, then layer in LLM and API analyzers for comprehensive protection.

---

**Script Location**: `scripts/python/scan_mcp_servers.py`
**MCP Scanner Version**: Latest (cisco-ai-mcp-scanner)

#!/usr/bin/env python3
"""
MCP Server Security Scanner

This script scans all MCP servers defined in a configuration file for security vulnerabilities.
It uses the Cisco AI Defense MCP Scanner library with multiple analysis engines:
- YARA: Pattern-based threat detection (no API key required)
- LLM: Semantic analysis using language models (optional, requires LLM API key)
- API: Cisco AI Defense Inspect API (optional, requires Cisco API key)

Usage:
    python scan_mcp_servers.py [--config PATH] [--analyzers yara,llm,api] [--output PATH]

Examples:
    # Scan with YARA only (default)
    python scan_mcp_servers.py

    # Scan with YARA and LLM analyzers
    python scan_mcp_servers.py --analyzers yara,llm

    # Scan with custom config file
    python scan_mcp_servers.py --config /path/to/.mcp.json --output results.json
"""

import asyncio
import json
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime

try:
    from mcpscanner import Config, Scanner
    from mcpscanner.core.models import AnalyzerEnum
    from mcpscanner.core.exceptions import MCPScannerError
    from mcpscanner.core.mcp_models import StdioServer
    from mcpscanner.core.auth import Auth, AuthType
except ImportError:
    print("ERROR: mcpscanner library not found!")
    print("Install it with: pip install cisco-ai-mcp-scanner")
    sys.exit(1)


class MCPSecurityScanner:
    """Comprehensive MCP server security scanner."""

    def __init__(
        self,
        config_path: Path,
        analyzers: List[AnalyzerEnum],
        api_key: Optional[str] = None,
        llm_api_key: Optional[str] = None,
    ):
        """Initialize the scanner.

        Args:
            config_path: Path to MCP configuration file (.mcp.json)
            analyzers: List of analyzers to use
            api_key: Optional Cisco AI Defense API key
            llm_api_key: Optional LLM provider API key
        """
        self.config_path = config_path
        self.analyzers = analyzers
        self.mcp_config = self._load_mcp_config()

        # Create scanner configuration
        scanner_config = Config(
            api_key=api_key,
            llm_provider_api_key=llm_api_key,
        )
        self.scanner = Scanner(scanner_config)

        # Results storage
        self.results: Dict[str, Any] = {
            "scan_timestamp": datetime.now().isoformat(),
            "config_file": str(config_path),
            "analyzers_used": [a.value for a in analyzers],
            "servers": {},
            "summary": {
                "total_servers": 0,
                "scanned_servers": 0,
                "failed_servers": 0,
                "total_tools": 0,
                "safe_tools": 0,
                "unsafe_tools": 0,
                "total_findings": 0,
            },
        }

    def _load_mcp_config(self) -> Dict[str, Any]:
        """Load MCP configuration from JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
                if "mcpServers" not in config:
                    raise ValueError("Invalid MCP config: missing 'mcpServers' key")
                return config
        except FileNotFoundError:
            print(f"ERROR: Config file not found: {self.config_path}")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"ERROR: Invalid JSON in config file: {e}")
            sys.exit(1)

    async def scan_stdio_server(self, server_name: str, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan a stdio MCP server.

        Args:
            server_name: Name of the server
            server_config: Server configuration dict

        Returns:
            Scan results for this server
        """
        print(f"\n📡 Scanning stdio server: {server_name}")
        print(f"   Command: {server_config.get('command')}")
        print(f"   Args: {server_config.get('args', [])}")

        result = {
            "server_type": "stdio",
            "command": server_config.get("command"),
            "args": server_config.get("args", []),
            "status": "pending",
            "tools": [],
            "error": None,
        }

        try:
            # Create StdioServer configuration
            stdio_server = StdioServer(
                command=server_config["command"],
                args=server_config.get("args", []),
                env=server_config.get("env"),
            )

            # Scan tools from stdio server
            tool_results = await self.scanner.scan_stdio_server_tools(
                server_config=stdio_server,
                analyzers=self.analyzers,
            )

            result["status"] = "completed"
            result["tools"] = self._process_tool_results(tool_results)

            safe_count = sum(1 for t in result["tools"] if t["is_safe"])
            unsafe_count = len(result["tools"]) - safe_count

            print(f"   ✅ Scanned {len(result['tools'])} tools")
            print(f"      Safe: {safe_count}, Unsafe: {unsafe_count}")

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            print(f"   ❌ Scan failed: {e}")

        return result

    async def scan_http_server(self, server_name: str, server_config: Dict[str, Any]) -> Dict[str, Any]:
        """Scan an HTTP/SSE MCP server.

        Args:
            server_name: Name of the server
            server_config: Server configuration dict

        Returns:
            Scan results for this server
        """
        print(f"\n📡 Scanning HTTP server: {server_name}")
        print(f"   URL: {server_config.get('url')}")

        result = {
            "server_type": "http",
            "url": server_config.get("url"),
            "status": "pending",
            "tools": [],
            "error": None,
        }

        try:
            # Extract bearer token from headers if present
            auth = None
            headers = server_config.get("headers", {})
            if "Authorization" in headers:
                auth_header = headers["Authorization"]
                if auth_header.startswith("Bearer "):
                    bearer_token = auth_header.replace("Bearer ", "")
                    auth = Auth(
                        auth_type=AuthType.BEARER,
                        bearer_token=bearer_token,
                    )

            # Scan tools from HTTP server
            tool_results = await self.scanner.scan_remote_server_tools(
                server_url=server_config["url"],
                analyzers=self.analyzers,
                auth=auth,
            )

            result["status"] = "completed"
            result["tools"] = self._process_tool_results(tool_results)

            safe_count = sum(1 for t in result["tools"] if t["is_safe"])
            unsafe_count = len(result["tools"]) - safe_count

            print(f"   ✅ Scanned {len(result['tools'])} tools")
            print(f"      Safe: {safe_count}, Unsafe: {unsafe_count}")

        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            print(f"   ❌ Scan failed: {e}")

        return result

    def _process_tool_results(self, tool_results: List[Any]) -> List[Dict[str, Any]]:
        """Process tool scan results into a serializable format."""
        processed = []

        for tool_result in tool_results:
            tool_data = {
                "name": tool_result.tool_name,
                "description": tool_result.tool_description,
                "is_safe": tool_result.is_safe,
                "status": tool_result.status,
                "findings": [],
                "analyzer_results": {},
            }

            # Process findings
            for finding in tool_result.findings:
                tool_data["findings"].append({
                    "severity": finding.severity.value if hasattr(finding.severity, 'value') else str(finding.severity),
                    "category": finding.category if hasattr(finding, 'category') else None,
                    "description": finding.description if hasattr(finding, 'description') else finding.summary,
                    "threat_names": finding.threat_names if hasattr(finding, 'threat_names') else [],
                })

            # Process analyzer-specific results
            if hasattr(tool_result, 'analyzer_results'):
                for analyzer_name, analyzer_result in tool_result.analyzer_results.items():
                    tool_data["analyzer_results"][analyzer_name] = {
                        "is_safe": analyzer_result.is_safe if hasattr(analyzer_result, 'is_safe') else True,
                        "findings_count": len(analyzer_result.findings) if hasattr(analyzer_result, 'findings') else 0,
                    }

            processed.append(tool_data)

        return processed

    async def scan_all_servers(self):
        """Scan all servers defined in the MCP configuration."""
        print("=" * 80)
        print("🔒 MCP SERVER SECURITY SCANNER")
        print("=" * 80)
        print(f"\nConfiguration: {self.config_path}")
        print(f"Analyzers: {', '.join(a.value for a in self.analyzers)}")
        print(f"Servers to scan: {len(self.mcp_config['mcpServers'])}")
        print("=" * 80)

        self.results["summary"]["total_servers"] = len(self.mcp_config["mcpServers"])

        for server_name, server_config in self.mcp_config["mcpServers"].items():
            server_type = server_config.get("type", "unknown")

            try:
                if server_type == "stdio":
                    server_result = await self.scan_stdio_server(server_name, server_config)
                elif server_type == "http":
                    server_result = await self.scan_http_server(server_name, server_config)
                else:
                    print(f"\n⚠️  Skipping {server_name}: unsupported type '{server_type}'")
                    server_result = {
                        "server_type": server_type,
                        "status": "skipped",
                        "error": f"Unsupported server type: {server_type}",
                        "tools": [],
                    }

                self.results["servers"][server_name] = server_result

                # Update summary statistics
                if server_result["status"] == "completed":
                    self.results["summary"]["scanned_servers"] += 1
                    self.results["summary"]["total_tools"] += len(server_result["tools"])
                    self.results["summary"]["safe_tools"] += sum(
                        1 for t in server_result["tools"] if t["is_safe"]
                    )
                    self.results["summary"]["unsafe_tools"] += sum(
                        1 for t in server_result["tools"] if not t["is_safe"]
                    )
                    self.results["summary"]["total_findings"] += sum(
                        len(t["findings"]) for t in server_result["tools"]
                    )
                elif server_result["status"] == "failed":
                    self.results["summary"]["failed_servers"] += 1

            except Exception as e:
                print(f"\n❌ Unexpected error scanning {server_name}: {e}")
                self.results["servers"][server_name] = {
                    "status": "error",
                    "error": str(e),
                    "tools": [],
                }
                self.results["summary"]["failed_servers"] += 1

    def print_summary(self):
        """Print scan summary."""
        print("\n" + "=" * 80)
        print("📊 SCAN SUMMARY")
        print("=" * 80)

        summary = self.results["summary"]
        print(f"\nServers:")
        print(f"  Total:    {summary['total_servers']}")
        print(f"  Scanned:  {summary['scanned_servers']}")
        print(f"  Failed:   {summary['failed_servers']}")

        print(f"\nTools:")
        print(f"  Total:    {summary['total_tools']}")
        print(f"  ✅ Safe:    {summary['safe_tools']}")
        print(f"  ⚠️  Unsafe:  {summary['unsafe_tools']}")

        print(f"\nFindings:")
        print(f"  Total security findings: {summary['total_findings']}")

        # List unsafe tools
        if summary['unsafe_tools'] > 0:
            print("\n" + "=" * 80)
            print("⚠️  UNSAFE TOOLS DETECTED")
            print("=" * 80)

            for server_name, server_result in self.results["servers"].items():
                unsafe_tools = [t for t in server_result.get("tools", []) if not t["is_safe"]]
                if unsafe_tools:
                    print(f"\n🔴 Server: {server_name}")
                    for tool in unsafe_tools:
                        print(f"   • {tool['name']}")
                        print(f"     Status: {tool['status']}")
                        print(f"     Findings: {len(tool['findings'])}")
                        for finding in tool['findings'][:3]:  # Show first 3 findings
                            print(f"       - [{finding['severity']}] {finding['description'][:80]}...")
                        if len(tool['findings']) > 3:
                            print(f"       ... and {len(tool['findings']) - 3} more findings")

    def save_results(self, output_path: Path):
        """Save scan results to JSON file."""
        try:
            with open(output_path, 'w') as f:
                json.dump(self.results, f, indent=2)
            print(f"\n💾 Results saved to: {output_path}")
        except Exception as e:
            print(f"\n❌ Failed to save results: {e}")


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Scan MCP servers for security vulnerabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Default to looking for .mcp.json in project root
    default_config = Path.cwd() / ".mcp.json"
    if not default_config.exists():
        # Try looking in parent directory
        default_config = Path.cwd().parent / ".mcp.json"

    parser.add_argument(
        "--config",
        type=Path,
        default=default_config,
        help="Path to MCP configuration file (default: .mcp.json in current or parent directory)",
    )

    parser.add_argument(
        "--analyzers",
        type=str,
        default="yara",
        help="Comma-separated list of analyzers to use: yara, llm, api (default: yara)",
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=Path("mcp_scan_results.json"),
        help="Path to save JSON results (default: mcp_scan_results.json)",
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="Cisco AI Defense API key (optional, for API analyzer)",
    )

    parser.add_argument(
        "--llm-api-key",
        type=str,
        help="LLM provider API key (optional, for LLM analyzer)",
    )

    args = parser.parse_args()

    # Parse analyzers
    analyzer_map = {
        "yara": AnalyzerEnum.YARA,
        "llm": AnalyzerEnum.LLM,
        "api": AnalyzerEnum.API,
    }

    analyzers = []
    for analyzer_name in args.analyzers.split(","):
        analyzer_name = analyzer_name.strip().lower()
        if analyzer_name in analyzer_map:
            analyzers.append(analyzer_map[analyzer_name])
        else:
            print(f"⚠️  Warning: Unknown analyzer '{analyzer_name}', skipping")

    if not analyzers:
        print("ERROR: No valid analyzers specified!")
        sys.exit(1)

    # Create scanner
    scanner = MCPSecurityScanner(
        config_path=args.config,
        analyzers=analyzers,
        api_key=args.api_key,
        llm_api_key=args.llm_api_key,
    )

    try:
        # Run scan
        await scanner.scan_all_servers()

        # Print summary
        scanner.print_summary()

        # Save results
        scanner.save_results(args.output)

        print("\n" + "=" * 80)
        print("✅ Scan completed successfully!")
        print("=" * 80)

    except KeyboardInterrupt:
        print("\n\n⚠️  Scan cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Scan failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())

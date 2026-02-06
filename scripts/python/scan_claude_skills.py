#!/usr/bin/env python3
"""
Claude Skills Security Scanner

This script uses cisco-ai-skill-scanner to scan Claude Code skills for security vulnerabilities,
including:
- Prompt injection attacks
- Data exfiltration patterns
- Malicious code execution
- Command injection
- Sensitive data exposure

Features:
- Multi-analyzer support (Static, Behavioral, LLM)
- Multiple output formats (JSON, Markdown, Table, SARIF)
- Detailed finding reports with severity levels
- Summary statistics and risk assessment

Usage:
    # Basic scan with static analyzer only
    python scan_claude_skills.py

    # Scan with behavioral analysis (dataflow)
    python scan_claude_skills.py --use-behavioral

    # Scan with all analyzers (requires SKILL_SCANNER_LLM_API_KEY env var)
    python scan_claude_skills.py --use-behavioral --use-llm

    # Generate detailed markdown report
    python scan_claude_skills.py --format markdown --output report.md

    # CI/CD mode - fail if critical/high findings
    python scan_claude_skills.py --fail-on-findings
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from skill_scanner import SkillScanner
from skill_scanner.core.analyzers.behavioral_analyzer import BehavioralAnalyzer
from skill_scanner.core.analyzers.static import StaticAnalyzer
from skill_scanner.core.models import Severity


def get_severity_emoji(severity: Severity) -> str:
    """Get emoji for severity level."""
    severity_emojis = {
        Severity.CRITICAL: "🔴",
        Severity.HIGH: "🟠",
        Severity.MEDIUM: "🟡",
        Severity.LOW: "🔵",
        Severity.INFO: "⚪",
        Severity.SAFE: "✅",
    }
    return severity_emojis.get(severity, "❓")


def print_banner():
    """Print banner."""
    print("=" * 80)
    print("   Claude Skills Security Scanner")
    print("   Powered by Cisco AI Defense Skill Scanner")
    print("=" * 80)
    print()


def print_finding_details(result):
    """Print detailed findings for a scan result."""
    if not result.findings:
        print(f"  ✅ No security issues found\n")
        return

    # Group findings by severity
    findings_by_severity = {
        Severity.CRITICAL: [],
        Severity.HIGH: [],
        Severity.MEDIUM: [],
        Severity.LOW: [],
        Severity.INFO: [],
    }

    for finding in result.findings:
        if finding.severity in findings_by_severity:
            findings_by_severity[finding.severity].append(finding)

    # Print findings by severity (highest first)
    for severity in [Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW, Severity.INFO]:
        findings = findings_by_severity[severity]
        if not findings:
            continue

        print(f"\n  {get_severity_emoji(severity)} {severity.value} Findings ({len(findings)}):")
        print("  " + "-" * 76)

        for finding in findings:
            print(f"\n    [{finding.severity.value}] {finding.title}")
            print(f"    Rule: {finding.rule_id}")

            if finding.description:
                # Wrap description
                desc_lines = finding.description.split('\n')
                for line in desc_lines:
                    if line.strip():
                        print(f"    Description: {line.strip()}")
                        break

            if finding.file_path:
                location = f"    Location: {finding.file_path}"
                if finding.line_number:
                    location += f":{finding.line_number}"
                print(location)

            if finding.snippet:
                # Show first line of snippet
                snippet_preview = finding.snippet.split('\n')[0][:60]
                if len(finding.snippet) > 60:
                    snippet_preview += "..."
                print(f"    Snippet: {snippet_preview}")


def print_summary_table(report):
    """Print summary table of all scanned skills."""
    print("\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Skill Name':<30} {'Status':<10} {'Severity':<10} {'Findings':<10}")
    print("-" * 80)

    for result in report.scan_results:
        status = "✅ SAFE" if result.is_safe else "⚠️  UNSAFE"
        severity_indicator = get_severity_emoji(result.max_severity)
        findings_count = len(result.findings)

        print(f"{result.skill_name:<30} {status:<10} {severity_indicator} {result.max_severity.value:<8} {findings_count:<10}")

    print("-" * 80)
    print(f"{'TOTAL':<30} {report.total_skills_scanned} skills")
    print()


def save_json_report(report, output_path: Path):
    """Save detailed JSON report."""
    report_data = {
        "scan_timestamp": datetime.now().isoformat(),
        "summary": {
            "total_skills": report.total_skills_scanned,
            "safe_count": report.safe_count,
            "unsafe_count": report.total_skills_scanned - report.safe_count,
            "total_findings": report.total_findings,
            "critical_count": report.critical_count,
            "high_count": report.high_count,
            "medium_count": report.medium_count,
            "low_count": report.low_count,
            "info_count": report.info_count,
        },
        "skills": []
    }

    for result in report.scan_results:
        skill_data = {
            "name": result.skill_name,
            "is_safe": result.is_safe,
            "max_severity": result.max_severity.value,
            "total_findings": len(result.findings),
            "findings": []
        }

        for finding in result.findings:
            finding_data = {
                "title": finding.title,
                "severity": finding.severity.value,
                "rule_id": finding.rule_id,
                "description": finding.description,
                "file_path": str(finding.file_path) if finding.file_path else None,
                "line_number": finding.line_number,
                "snippet": finding.snippet,
                "category": finding.category,
            }
            skill_data["findings"].append(finding_data)

        report_data["skills"].append(skill_data)

    with open(output_path, 'w') as f:
        json.dump(report_data, f, indent=2)

    print(f"\n✅ JSON report saved to: {output_path}")


def save_markdown_report(report, output_path: Path):
    """Save detailed markdown report."""
    md_lines = [
        "# Claude Skills Security Scan Report",
        f"\n**Scan Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"\n## Summary",
        f"\n- **Total Skills Scanned:** {report.total_skills_scanned}",
        f"- **Safe Skills:** {report.safe_count}",
        f"- **Unsafe Skills:** {report.total_skills_scanned - report.safe_count}",
        f"- **Total Findings:** {report.total_findings}",
        f"\n### Severity Breakdown",
        f"\n| Severity | Count |",
        f"|----------|-------|",
    ]

    if report.critical_count > 0:
        md_lines.append(f"| 🔴 CRITICAL | {report.critical_count} |")
    if report.high_count > 0:
        md_lines.append(f"| 🟠 HIGH | {report.high_count} |")
    if report.medium_count > 0:
        md_lines.append(f"| 🟡 MEDIUM | {report.medium_count} |")
    if report.low_count > 0:
        md_lines.append(f"| 🔵 LOW | {report.low_count} |")
    if report.info_count > 0:
        md_lines.append(f"| ⚪ INFO | {report.info_count} |")

    md_lines.append("\n## Detailed Results\n")

    for result in report.scan_results:
        status = "✅ SAFE" if result.is_safe else "⚠️ UNSAFE"
        md_lines.append(f"\n### {result.skill_name} - {status}")
        md_lines.append(f"\n- **Max Severity:** {get_severity_emoji(result.max_severity)} {result.max_severity.value}")
        md_lines.append(f"- **Total Findings:** {len(result.findings)}")

        if result.findings:
            md_lines.append("\n#### Findings\n")

            for finding in result.findings:
                md_lines.append(f"\n##### {get_severity_emoji(finding.severity)} [{finding.severity.value}] {finding.title}")
                md_lines.append(f"\n- **Rule ID:** `{finding.rule_id}`")

                if finding.description:
                    md_lines.append(f"- **Description:** {finding.description}")

                if finding.file_path:
                    location = f"`{finding.file_path}`"
                    if finding.line_number:
                        location += f" (line {finding.line_number})"
                    md_lines.append(f"- **Location:** {location}")

                if finding.snippet:
                    md_lines.append(f"- **Code Snippet:**\n  ```\n  {finding.snippet[:200]}\n  ```")

    md_lines.append("\n---\n*Generated by Cisco AI Defense Skill Scanner*")

    with open(output_path, 'w') as f:
        f.write('\n'.join(md_lines))

    print(f"✅ Markdown report saved to: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Scan Claude Code skills for security vulnerabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        "--skills-dir",
        type=str,
        default=".claude/skills",
        help="Path to Claude skills directory (default: .claude/skills)"
    )

    parser.add_argument(
        "--use-behavioral",
        action="store_true",
        help="Enable behavioral analyzer (AST dataflow analysis)"
    )

    parser.add_argument(
        "--use-llm",
        action="store_true",
        help="Enable LLM analyzer (requires SKILL_SCANNER_LLM_API_KEY)"
    )

    parser.add_argument(
        "--format",
        choices=["summary", "json", "markdown", "both"],
        default="summary",
        help="Output format (default: summary)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output file path (auto-generates if not specified)"
    )

    parser.add_argument(
        "--fail-on-findings",
        action="store_true",
        help="Exit with code 1 if CRITICAL or HIGH findings are found"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        default=True,
        help="Scan skills recursively (default: True)"
    )

    args = parser.parse_args()

    # Resolve skills directory path
    skills_dir = Path(args.skills_dir)
    if not skills_dir.is_absolute():
        skills_dir = Path.cwd() / skills_dir

    if not skills_dir.exists():
        print(f"❌ Error: Skills directory not found: {skills_dir}")
        return 1

    print_banner()
    print(f"📁 Skills Directory: {skills_dir}")
    print(f"🔍 Recursive Scan: {args.recursive}")

    # Setup analyzers
    analyzers = [StaticAnalyzer()]
    analyzer_names = ["Static (YAML+YARA)"]

    if args.use_behavioral:
        analyzers.append(BehavioralAnalyzer(use_static_analysis=True))
        analyzer_names.append("Behavioral (Dataflow)")

    if args.use_llm:
        api_key = os.getenv("SKILL_SCANNER_LLM_API_KEY")
        if not api_key:
            print("⚠️  Warning: --use-llm specified but SKILL_SCANNER_LLM_API_KEY not set")
            print("    Skipping LLM analyzer. Set environment variable to enable.")
        else:
            try:
                from skill_scanner.core.analyzers.llm_analyzer import LLMAnalyzer
                analyzers.append(LLMAnalyzer())
                analyzer_names.append("LLM (Semantic)")
            except ImportError as e:
                print(f"⚠️  Warning: Could not import LLM analyzer: {e}")

    print(f"🔬 Analyzers: {', '.join(analyzer_names)}")
    print()

    # Create scanner
    scanner = SkillScanner(analyzers=analyzers)

    # Scan directory
    print("🚀 Starting scan...\n")
    try:
        report = scanner.scan_directory(skills_dir, recursive=args.recursive)
    except Exception as e:
        print(f"❌ Error during scan: {e}")
        import traceback
        traceback.print_exc()
        return 1

    # Print results
    print("=" * 80)
    print("SCAN RESULTS")
    print("=" * 80)
    print(f"Total Skills Scanned: {report.total_skills_scanned}")
    print(f"Safe Skills: {report.safe_count} ✅")
    print(f"Unsafe Skills: {report.total_skills_scanned - report.safe_count} ⚠️")
    print(f"Total Findings: {report.total_findings}")

    if report.total_findings > 0:
        print("\nSeverity Breakdown:")
        if report.critical_count > 0:
            print(f"  🔴 CRITICAL: {report.critical_count}")
        if report.high_count > 0:
            print(f"  🟠 HIGH: {report.high_count}")
        if report.medium_count > 0:
            print(f"  🟡 MEDIUM: {report.medium_count}")
        if report.low_count > 0:
            print(f"  🔵 LOW: {report.low_count}")
        if report.info_count > 0:
            print(f"  ⚪ INFO: {report.info_count}")

    # Print detailed results for each skill
    print("\n" + "=" * 80)
    print("DETAILED FINDINGS")
    print("=" * 80)

    for result in report.scan_results:
        status = "✅ SAFE" if result.is_safe else "⚠️  UNSAFE"
        print(f"\n📦 Skill: {result.skill_name} - {status}")
        print(f"   Max Severity: {get_severity_emoji(result.max_severity)} {result.max_severity.value}")
        print(f"   Total Findings: {len(result.findings)}")

        print_finding_details(result)

    # Print summary table
    print_summary_table(report)

    # Save reports
    if args.format in ["json", "both"]:
        if args.output:
            # If output specified, use it with .json extension
            output_path = Path(args.output)
            if output_path.suffix != '.json':
                output_path = output_path.with_suffix('.json')
        else:
            output_path = Path(f"skill_scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_json_report(report, output_path)

    if args.format in ["markdown", "both"]:
        if args.output:
            # If output specified, use it with .md extension
            output_path = Path(args.output)
            if output_path.suffix not in ['.md', '.markdown']:
                if args.format == "both":
                    # For both format, append _report.md
                    output_path = output_path.parent / f"{output_path.stem}.md"
                else:
                    output_path = output_path.with_suffix('.md')
        else:
            output_path = Path(f"skill_scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md")

        # Ensure parent directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        save_markdown_report(report, output_path)

    # Check for critical/high findings
    has_critical_or_high = report.critical_count > 0 or report.high_count > 0

    if args.fail_on_findings and has_critical_or_high:
        print("\n❌ SCAN FAILED: Critical or High severity findings detected")
        return 1

    print("\n✅ Scan completed successfully")
    return 0


if __name__ == "__main__":
    sys.exit(main())

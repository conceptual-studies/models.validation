#!/usr/bin/env python3
"""
FCM Repository Auto-Remediation Tool
Implementation of Layer 4 automated remediation from the GitHub Repository Model
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class RemediationAction:
    """Single remediation action"""
    action_type: str  # create_file, create_directory, fix_content, rename, etc.
    description: str
    target_path: str
    safety_level: str  # safe, caution, risky
    content: Optional[str] = None
    backup_needed: bool = False


@dataclass
class RemediationPlan:
    """Complete remediation plan"""
    actions: List[RemediationAction]
    safety_summary: Dict[str, int]
    estimated_time: str
    prerequisites: List[str]
    warnings: List[str]


class FCMAutoRemediation:
    """
    Automated remediation implementing Layer 4 enforcement mechanisms
    """
    
    def __init__(self, repo_path: str, safe_mode: bool = True):
        """Initialize remediation system"""
        self.repo_path = Path(repo_path)
        self.safe_mode = safe_mode
        self.backup_dir = self.repo_path / ".remediation_backups"
        self.templates = self._load_templates()
    
    def _load_templates(self) -> Dict[str, str]:
        """Load file templates for creation"""
        return {
            "README.md": """# {repository_name}

## Overview

Brief description of this FCM repository.

## Usage

Instructions for using the models and systems in this repository.

## Contributing

Guidelines for contributing to this repository.

## Links

- [FCM Documentation](https://formal-conceptual-models.org)
""",
            
            "LICENSE": """MIT License

Copyright (c) {year} {organization}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
            
            "fcm.manifest.json": """{
  "$schema": "https://formal-conceptual-models.org/schemas/manifest-v2.json",
  "type": "fcm-repository",
  "category": "{repository_type}",
  "name": "{repository_name}",
  "description": "FCM repository for {repository_type} models",
  "version": "1.0.0",
  "fcm-core-version": ">=2.0.0",
  "created": "{date}",
  "updated": "{date}",
  "maintainers": [
    {
      "name": "Repository Maintainer",
      "role": "primary"
    }
  ],
  "license": "MIT",
  "keywords": ["fcm", "{repository_type}"],
  "maturity": "beta",
  "exports": [],
  "quality": {
    "fcm-compliance": true,
    "has-tests": false,
    "has-examples": false,
    "documentation-complete": false
  }
}""",
            
            "SECURITY.md": """# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in this repository, please report it by:

1. **Do not** create a public GitHub issue
2. Email the maintainers directly (see fcm.manifest.json for contact info)
3. Include details about the vulnerability and steps to reproduce

We will respond within 48 hours and work with you to address the issue promptly.

## Security Best Practices

This repository follows FCM security guidelines:
- Regular dependency updates
- Automated security scanning
- Access control policies
- Secure development practices
""",
            
            ".github/dependabot.yml": """version: 2
updates:
  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
"""
        }
    
    def analyze_violations(self, validation_result: Dict[str, Any]) -> RemediationPlan:
        """Analyze validation violations and create remediation plan"""
        violations = validation_result.get("violations", [])
        actions = []
        
        for violation in violations:
            remediation_actions = self._create_actions_for_violation(violation)
            actions.extend(remediation_actions)
        
        # Create plan
        plan = RemediationPlan(
            actions=actions,
            safety_summary=self._analyze_safety(actions),
            estimated_time=self._estimate_time(actions),
            prerequisites=self._check_prerequisites(),
            warnings=self._generate_warnings(actions)
        )
        
        return plan
    
    def _create_actions_for_violation(self, violation: str) -> List[RemediationAction]:
        """Create specific remediation actions for a violation"""
        actions = []
        
        if "Missing required directory" in violation:
            dir_name = violation.split(": ")[-1]
            actions.append(RemediationAction(
                action_type="create_directory",
                description=f"Create required directory: {dir_name}",
                target_path=dir_name,
                safety_level="safe"
            ))
            
            # Add README to directory if it's a major directory
            if dir_name in ["core", "composite", "bridges", "analytical", "empirical"]:
                readme_path = f"{dir_name}/README.md"
                actions.append(RemediationAction(
                    action_type="create_file",
                    description=f"Create directory README: {readme_path}",
                    target_path=readme_path,
                    safety_level="safe",
                    content=f"# {dir_name.title()}\n\nContent for {dir_name} directory.\n"
                ))
        
        elif "Missing required file" in violation:
            file_name = violation.split(": ")[-1]
            
            if file_name in self.templates:
                actions.append(RemediationAction(
                    action_type="create_file",
                    description=f"Create required file: {file_name}",
                    target_path=file_name,
                    safety_level="safe",
                    content=self._render_template(file_name)
                ))
            else:
                actions.append(RemediationAction(
                    action_type="create_file",
                    description=f"Create required file: {file_name}",
                    target_path=file_name,
                    safety_level="caution",
                    content=f"# {file_name}\n\nGenerated file - please customize.\n"
                ))
        
        elif "README.md" in violation and "too short" in violation:
            actions.append(RemediationAction(
                action_type="fix_content",
                description="Expand README.md content",
                target_path="README.md",
                safety_level="caution",
                backup_needed=True,
                content=self._render_template("README.md")
            ))
        
        elif "manifest" in violation and "missing" in violation:
            actions.append(RemediationAction(
                action_type="create_file",
                description="Create FCM manifest file",
                target_path="fcm.manifest.json",
                safety_level="safe",
                content=self._render_template("fcm.manifest.json")
            ))
        
        elif "naming convention" in violation:
            # Extract the problematic file/directory name
            if "Model file" in violation:
                # Handle FCM model naming issues
                actions.append(RemediationAction(
                    action_type="rename",
                    description="Fix FCM model file naming",
                    target_path="",  # Would need to extract specific file
                    safety_level="risky",
                    backup_needed=True
                ))
        
        elif "security policy" in violation:
            actions.append(RemediationAction(
                action_type="create_file",
                description="Create security policy",
                target_path="SECURITY.md",
                safety_level="safe",
                content=self.templates["SECURITY.md"]
            ))
        
        elif "dependency scanning" in violation:
            actions.append(RemediationAction(
                action_type="create_file",
                description="Setup dependency scanning",
                target_path=".github/dependabot.yml",
                safety_level="safe",
                content=self.templates[".github/dependabot.yml"]
            ))
            
            # Ensure .github directory exists
            actions.insert(-1, RemediationAction(
                action_type="create_directory",
                description="Create .github directory",
                target_path=".github",
                safety_level="safe"
            ))
        
        return actions
    
    def _render_template(self, template_name: str) -> str:
        """Render template with repository-specific variables"""
        template = self.templates.get(template_name, "")
        
        # Get repository info
        repo_name = self.repo_path.name
        repo_type = self._detect_repository_type()
        
        # Template variables
        variables = {
            "repository_name": repo_name,
            "repository_type": repo_type,
            "organization": "FCM Organization",  # Could be detected from git config
            "year": str(datetime.now().year),
            "date": datetime.now().isoformat()[:10]
        }
        
        # Replace variables
        for var, value in variables.items():
            template = template.replace(f"{{{var}}}", value)
        
        return template
    
    def _detect_repository_type(self) -> str:
        """Detect repository type from structure"""
        if (self.repo_path / "core").exists():
            return "framework"
        elif (self.repo_path / "analytical").exists() or (self.repo_path / "empirical").exists():
            return "systems"
        elif (self.repo_path / "experiments").exists():
            return "lab"
        else:
            return "personal"
    
    def _analyze_safety(self, actions: List[RemediationAction]) -> Dict[str, int]:
        """Analyze safety levels of all actions"""
        safety_counts = {"safe": 0, "caution": 0, "risky": 0}
        
        for action in actions:
            safety_counts[action.safety_level] += 1
        
        return safety_counts
    
    def _estimate_time(self, actions: List[RemediationAction]) -> str:
        """Estimate time required for all actions"""
        total_minutes = 0
        
        for action in actions:
            if action.action_type == "create_file":
                total_minutes += 2
            elif action.action_type == "create_directory":
                total_minutes += 1
            elif action.action_type == "fix_content":
                total_minutes += 5
            elif action.action_type == "rename":
                total_minutes += 3
        
        if total_minutes < 5:
            return "< 5 minutes"
        elif total_minutes < 15:
            return "5-15 minutes"
        elif total_minutes < 30:
            return "15-30 minutes"
        else:
            return "30+ minutes"
    
    def _check_prerequisites(self) -> List[str]:
        """Check prerequisites for remediation"""
        prerequisites = []
        
        # Check if in git repository
        if not (self.repo_path / ".git").exists():
            prerequisites.append("Repository must be a Git repository")
        
        # Check write permissions
        if not os.access(self.repo_path, os.W_OK):
            prerequisites.append("Write permissions required for repository")
        
        return prerequisites
    
    def _generate_warnings(self, actions: List[RemediationAction]) -> List[str]:
        """Generate warnings about remediation actions"""
        warnings = []
        
        risky_actions = [a for a in actions if a.safety_level == "risky"]
        if risky_actions:
            warnings.append(f"{len(risky_actions)} risky action(s) require manual review")
        
        backup_actions = [a for a in actions if a.backup_needed]
        if backup_actions:
            warnings.append(f"{len(backup_actions)} action(s) will modify existing files")
        
        return warnings
    
    def execute_plan(self, plan: RemediationPlan, safety_filter: str = "safe") -> Dict[str, Any]:
        """Execute remediation plan with safety filtering"""
        results = {
            "executed": [],
            "skipped": [],
            "errors": [],
            "total_actions": len(plan.actions)
        }
        
        # Create backup directory if needed
        backup_actions = [a for a in plan.actions if a.backup_needed]
        if backup_actions:
            self._create_backup_directory()
        
        # Filter actions by safety level
        if safety_filter == "safe":
            allowed_levels = ["safe"]
        elif safety_filter == "caution":
            allowed_levels = ["safe", "caution"]
        else:  # "risky"
            allowed_levels = ["safe", "caution", "risky"]
        
        for action in plan.actions:
            if action.safety_level not in allowed_levels:
                results["skipped"].append({
                    "action": action.description,
                    "reason": f"Safety level {action.safety_level} not allowed"
                })
                continue
            
            try:
                self._execute_action(action)
                results["executed"].append(action.description)
            except Exception as e:
                results["errors"].append({
                    "action": action.description,
                    "error": str(e)
                })
        
        return results
    
    def _execute_action(self, action: RemediationAction):
        """Execute a single remediation action"""
        target_path = self.repo_path / action.target_path
        
        if action.action_type == "create_directory":
            target_path.mkdir(parents=True, exist_ok=True)
        
        elif action.action_type == "create_file":
            # Create parent directories if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Don't overwrite existing files unless explicitly allowed
            if target_path.exists() and not action.backup_needed:
                raise FileExistsError(f"File already exists: {target_path}")
            
            # Create backup if needed
            if target_path.exists() and action.backup_needed:
                self._create_backup(target_path)
            
            # Write content
            with open(target_path, 'w') as f:
                f.write(action.content or "")
        
        elif action.action_type == "fix_content":
            if not target_path.exists():
                raise FileNotFoundError(f"File not found: {target_path}")
            
            # Create backup
            if action.backup_needed:
                self._create_backup(target_path)
            
            # Write new content
            with open(target_path, 'w') as f:
                f.write(action.content or "")
        
        elif action.action_type == "rename":
            # This would need more specific implementation
            # based on the actual naming issue
            pass
    
    def _create_backup_directory(self):
        """Create backup directory for modified files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / timestamp
        backup_path.mkdir(parents=True, exist_ok=True)
        return backup_path
    
    def _create_backup(self, file_path: Path):
        """Create backup of a file before modification"""
        if not self.backup_dir.exists():
            backup_dir = self._create_backup_directory()
        else:
            # Use most recent backup directory
            backup_dirs = sorted(self.backup_dir.glob("*"))
            backup_dir = backup_dirs[-1] if backup_dirs else self._create_backup_directory()
        
        # Preserve directory structure in backup
        relative_path = file_path.relative_to(self.repo_path)
        backup_file = backup_dir / relative_path
        backup_file.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(file_path, backup_file)
    
    def dry_run(self, plan: RemediationPlan) -> str:
        """Generate dry run report showing what would be done"""
        report = []
        report.append("# FCM Auto-Remediation Dry Run")
        report.append("=" * 40)
        report.append("")
        report.append(f"**Repository:** {self.repo_path}")
        report.append(f"**Total Actions:** {len(plan.actions)}")
        report.append(f"**Estimated Time:** {plan.estimated_time}")
        report.append("")
        
        # Safety summary
        report.append("## Safety Summary")
        for level, count in plan.safety_summary.items():
            if count > 0:
                report.append(f"- **{level.title()}:** {count} action(s)")
        report.append("")
        
        # Prerequisites
        if plan.prerequisites:
            report.append("## Prerequisites")
            for prereq in plan.prerequisites:
                report.append(f"- ❗ {prereq}")
            report.append("")
        
        # Warnings
        if plan.warnings:
            report.append("## Warnings")
            for warning in plan.warnings:
                report.append(f"- ⚠️ {warning}")
            report.append("")
        
        # Actions by safety level
        for safety_level in ["safe", "caution", "risky"]:
            level_actions = [a for a in plan.actions if a.safety_level == safety_level]
            if level_actions:
                report.append(f"## {safety_level.title()} Actions ({len(level_actions)})")
                for action in level_actions:
                    backup_note = " (with backup)" if action.backup_needed else ""
                    report.append(f"- **{action.action_type}**: {action.description}{backup_note}")
                report.append("")
        
        return "\n".join(report)


def main():
    """CLI interface for auto-remediation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FCM Repository Auto-Remediation")
    parser.add_argument("repo_path", help="Path to repository")
    parser.add_argument("--validation-result", help="Path to validation result JSON")
    parser.add_argument("--safety-level", choices=["safe", "caution", "risky"], default="safe")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without executing")
    parser.add_argument("--safe-only", action="store_true", help="Only execute safe actions")
    
    args = parser.parse_args()
    
    # Initialize remediation system
    remediation = FCMAutoRemediation(args.repo_path, safe_mode=True)
    
    # Load validation result
    if args.validation_result and Path(args.validation_result).exists():
        with open(args.validation_result, 'r') as f:
            validation_result = json.load(f)
    else:
        # Run quick validation
        from ..validators.repo_validator import FCMRepositoryValidator
        validator = FCMRepositoryValidator()
        result = validator.validate_repository(args.repo_path)
        validation_result = {
            "violations": result.violations,
            "score": result.score
        }
    
    # Create remediation plan
    plan = remediation.analyze_violations(validation_result)
    
    if args.dry_run:
        print(remediation.dry_run(plan))
    else:
        safety_filter = "safe" if args.safe_only else args.safety_level
        print(f"Executing remediation plan (safety level: {safety_filter})...")
        
        results = remediation.execute_plan(plan, safety_filter)
        
        print(f"Remediation completed:")
        print(f"  Executed: {len(results['executed'])} actions")
        print(f"  Skipped: {len(results['skipped'])} actions") 
        print(f"  Errors: {len(results['errors'])} actions")
        
        if results['errors']:
            print("\nErrors:")
            for error in results['errors']:
                print(f"  ❌ {error['action']}: {error['error']}")


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
FCM Repository Validator
Implementation of Layer 3 validation algorithms from the GitHub Repository Model
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class ComplianceLevel(Enum):
    """Repository compliance levels from the formal model"""
    BASIC = 0       # README, LICENSE exist
    STRUCTURED = 1  # proper directory hierarchy
    DOCUMENTED = 2  # complete documentation
    TESTED = 3      # automated testing present
    SECURE = 4      # security policies implemented
    EXEMPLARY = 5   # organizational best practices


@dataclass
class ValidationResult:
    """Result of repository validation"""
    score: float
    violations: List[str] = field(default_factory=list)
    compliance_level: ComplianceLevel = ComplianceLevel.BASIC
    recommendations: List[str] = field(default_factory=list)
    health_metrics: Dict[str, float] = field(default_factory=dict)


@dataclass
class RepositorySchema:
    """Repository validation schema"""
    repository_type: str
    required_directories: List[str]
    required_files: List[str]
    naming_conventions: Dict[str, str]
    content_requirements: Dict[str, Any]
    special_requirements: Dict[str, bool] = field(default_factory=dict)


class FCMRepositoryValidator:
    """
    Main repository validator implementing the GitHub Repository Model
    """
    
    def __init__(self, schema_path: str = "schemas/fcm-repository.json"):
        """Initialize validator with schema"""
        self.schema = self._load_schema(schema_path)
        self.repo_schemas = self._load_repository_schemas()
    
    def _load_schema(self, schema_path: str) -> Dict[str, Any]:
        """Load validation schema from JSON file"""
        with open(schema_path, 'r') as f:
            return json.load(f)
    
    def _load_repository_schemas(self) -> Dict[str, RepositorySchema]:
        """Load repository type-specific schemas"""
        schemas = {}
        repo_schemas = self.schema.get("repository_schemas", {})
        
        for repo_type, config in repo_schemas.items():
            schemas[repo_type] = RepositorySchema(
                repository_type=repo_type,
                required_directories=config.get("required_directories", []),
                required_files=config.get("required_files", []),
                naming_conventions=config.get("naming_conventions", {}),
                content_requirements=config.get("content_requirements", {}),
                special_requirements=config.get("special_requirements", {})
            )
        
        return schemas
    
    def validate_repository(self, repo_path: str, repo_type: str = None) -> ValidationResult:
        """
        Main validation function implementing Layer 3 algorithms
        """
        repo_path = Path(repo_path)
        
        # Auto-detect repository type if not provided
        if not repo_type:
            repo_type = self._detect_repository_type(repo_path)
        
        if repo_type not in self.repo_schemas:
            raise ValueError(f"Unknown repository type: {repo_type}")
        
        schema = self.repo_schemas[repo_type]
        
        # Layer 3 Algorithm: Structure validation
        structural_score, structural_violations = self._validate_structure(repo_path, schema)
        
        # Layer 3 Algorithm: Content validation  
        content_score, content_violations = self._validate_content(repo_path, schema)
        
        # Layer 3 Algorithm: Process validation
        process_score, process_violations = self._validate_processes(repo_path, schema)
        
        # Layer 3 Algorithm: Security validation
        security_score, security_violations = self._validate_security(repo_path, schema)
        
        # Calculate overall score using weights from schema
        # Default weights if not specified in schema
        default_weights = {
            "structural": 0.3,
            "content": 0.3,
            "process": 0.2,
            "security": 0.2
        }
        
        # Try to get weights from schema, fallback to defaults
        validation_rules = self.schema.get("validation_rules", {})
        weights = {
            "structural": validation_rules.get("structural", {}).get("weight", default_weights["structural"]),
            "content": validation_rules.get("content", {}).get("weight", default_weights["content"]),
            "process": validation_rules.get("process", {}).get("weight", default_weights["process"]),
            "security": validation_rules.get("security", {}).get("weight", default_weights["security"])
        }
        
        overall_score = (
            structural_score * weights["structural"] +
            content_score * weights["content"] +
            process_score * weights["process"] +
            security_score * weights["security"]
        )
        
        # Create ValidationResult with calculated score
        result = ValidationResult(score=overall_score)
        
        # Combine all violations
        result.violations.extend(structural_violations)
        result.violations.extend(content_violations)
        result.violations.extend(process_violations)
        result.violations.extend(security_violations)
        
        # Determine compliance level
        result.compliance_level = self._determine_compliance_level(result.score, result.violations)
        
        # Generate recommendations
        result.recommendations = self._generate_recommendations(result.violations, schema)
        
        # Calculate health metrics
        result.health_metrics = {
            "structural_health": structural_score,
            "content_health": content_score,
            "process_health": process_score,
            "security_health": security_score,
            "overall_health": result.score
        }
        
        return result
    
    def _detect_repository_type(self, repo_path: Path) -> str:
        """Auto-detect repository type from manifest or structure"""
        manifest_path = repo_path / "fcm.manifest.json"
        
        if manifest_path.exists():
            try:
                with open(manifest_path, 'r') as f:
                    manifest = json.load(f)
                    return manifest.get("category", "personal")
            except (json.JSONDecodeError, KeyError):
                pass
        
        # Fallback to structure-based detection
        if (repo_path / "core").exists() and (repo_path / "composite").exists():
            return "framework"
        elif (repo_path / "analytical").exists() or (repo_path / "empirical").exists():
            return "systems"
        elif (repo_path / "experiments").exists():
            return "lab"
        else:
            return "personal"
    
    def _validate_structure(self, repo_path: Path, schema: RepositorySchema) -> Tuple[float, List[str]]:
        """
        Implement structure validation algorithm from Layer 3
        """
        score = 0
        max_score = 0
        violations = []
        
        # Check required directories
        for dir_name in schema.required_directories:
            max_score += 1
            dir_path = repo_path / dir_name
            if dir_path.exists() and dir_path.is_dir():
                score += 1
            else:
                violations.append(f"Missing required directory: {dir_name}")
        
        # Check required files
        for file_name in schema.required_files:
            max_score += 1
            file_path = repo_path / file_name
            if file_path.exists() and file_path.is_file():
                score += 1
            else:
                violations.append(f"Missing required file: {file_name}")
        
        # Check naming conventions
        naming_violations = self._check_naming_conventions(repo_path, schema.naming_conventions)
        violations.extend(naming_violations)
        
        # Calculate score as percentage
        if max_score > 0:
            return score / max_score, violations
        else:
            return 1.0, violations
    
    def _validate_content(self, repo_path: Path, schema: RepositorySchema) -> Tuple[float, List[str]]:
        """Validate content requirements"""
        score = 0
        max_score = 0
        violations = []
        
        # Check README.md content
        readme_path = repo_path / "README.md"
        if readme_path.exists():
            max_score += 1
            readme_valid, readme_violations = self._validate_readme(readme_path)
            if readme_valid:
                score += 1
            else:
                violations.extend(readme_violations)
        
        # Check manifest content
        manifest_path = repo_path / "fcm.manifest.json"
        if manifest_path.exists():
            max_score += 1
            manifest_valid, manifest_violations = self._validate_manifest(manifest_path)
            if manifest_valid:
                score += 1
            else:
                violations.extend(manifest_violations)
        
        # Check FCM model compliance
        model_files = list(repo_path.rglob("fcm.*.md"))
        if model_files:
            max_score += 1
            models_valid, model_violations = self._validate_fcm_models(model_files)
            if models_valid:
                score += 1
            else:
                violations.extend(model_violations)
        
        if max_score > 0:
            return score / max_score, violations
        else:
            return 1.0, violations
    
    def _validate_processes(self, repo_path: Path, schema: RepositorySchema) -> Tuple[float, List[str]]:
        """Validate CI/CD and automation processes"""
        score = 0
        max_score = 3
        violations = []
        
        # Check for GitHub workflows
        workflows_dir = repo_path / ".github" / "workflows"
        if workflows_dir.exists() and list(workflows_dir.glob("*.yml")):
            score += 1
        else:
            violations.append("No GitHub workflows found")
        
        # Check for validation scripts
        if (repo_path / "validation").exists() or (repo_path / "tools").exists():
            score += 1
        else:
            violations.append("No validation tools found")
        
        # Check for automation indicators
        if (repo_path / "scripts").exists() or (repo_path / "Makefile").exists():
            score += 1
        else:
            violations.append("No automation scripts found")
        
        return score / max_score, violations
    
    def _validate_security(self, repo_path: Path, schema: RepositorySchema) -> Tuple[float, List[str]]:
        """Validate security policies and configurations"""
        score = 0
        max_score = 2
        violations = []
        
        # Check for security policy
        security_files = ["SECURITY.md", ".github/SECURITY.md", "docs/SECURITY.md"]
        if any((repo_path / f).exists() for f in security_files):
            score += 1
        else:
            violations.append("No security policy found")
        
        # Check for dependency scanning
        if (repo_path / ".github" / "dependabot.yml").exists():
            score += 1
        else:
            violations.append("No dependency scanning configured")
        
        return score / max_score, violations
    
    def _check_naming_conventions(self, repo_path: Path, conventions: Dict[str, str]) -> List[str]:
        """Check naming convention compliance"""
        violations = []
        
        # Check FCM model naming
        model_files = list(repo_path.rglob("fcm.*.md"))
        for model_file in model_files:
            if not re.match(r"^fcm\.[a-z]+(-[a-z]+)*\.md$", model_file.name):
                violations.append(f"Model file {model_file.name} doesn't follow FCM naming convention")
        
        # Check directory naming (should be lowercase)
        for item in repo_path.rglob("*"):
            if item.is_dir() and item.name != item.name.lower():
                violations.append(f"Directory {item.name} should be lowercase")
        
        return violations
    
    def _validate_readme(self, readme_path: Path) -> Tuple[bool, List[str]]:
        """Validate README.md content"""
        violations = []
        
        try:
            content = readme_path.read_text()
            
            # Check minimum length
            if len(content) < 100:
                violations.append("README.md is too short (minimum 100 characters)")
            
            # Check for required sections
            required_sections = ["#", "##"]  # At least title and one section
            has_sections = any(section in content for section in required_sections)
            if not has_sections:
                violations.append("README.md missing proper markdown sections")
            
            return len(violations) == 0, violations
            
        except Exception as e:
            return False, [f"Error reading README.md: {str(e)}"]
    
    def _validate_manifest(self, manifest_path: Path) -> Tuple[bool, List[str]]:
        """Validate fcm.manifest.json content"""
        violations = []
        
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            # Check required fields
            required_fields = ["type", "category", "name", "version"]
            for field in required_fields:
                if field not in manifest:
                    violations.append(f"Manifest missing required field: {field}")
            
            # Validate repository type
            if "category" in manifest:
                valid_categories = ["framework", "systems", "domains", "works", "projects", "lab", "personal"]
                if manifest["category"] not in valid_categories:
                    violations.append(f"Invalid repository category: {manifest['category']}")
            
            return len(violations) == 0, violations
            
        except json.JSONDecodeError as e:
            return False, [f"Invalid JSON in manifest: {str(e)}"]
        except Exception as e:
            return False, [f"Error reading manifest: {str(e)}"]
    
    def _validate_fcm_models(self, model_files: List[Path]) -> Tuple[bool, List[str]]:
        """Validate FCM model format compliance"""
        violations = []
        
        for model_file in model_files:
            try:
                content = model_file.read_text()
                
                # Check for Model ID
                if "**Model ID**:" not in content and "model_id:" not in content:
                    violations.append(f"{model_file.name} missing Model ID")
                
                # Check for Layer structure (basic FCM format check)
                if "## Layer 1:" not in content:
                    violations.append(f"{model_file.name} missing FCM layer structure")
                
            except Exception as e:
                violations.append(f"Error reading {model_file.name}: {str(e)}")
        
        return len(violations) == 0, violations
    
    def _determine_compliance_level(self, score: float, violations: List[str]) -> ComplianceLevel:
        """Determine compliance level based on score and violations"""
        if score >= 0.9 and len(violations) == 0:
            return ComplianceLevel.EXEMPLARY
        elif score >= 0.8:
            return ComplianceLevel.SECURE
        elif score >= 0.6:
            return ComplianceLevel.TESTED
        elif score >= 0.4:
            return ComplianceLevel.DOCUMENTED
        elif score >= 0.2:
            return ComplianceLevel.STRUCTURED
        else:
            return ComplianceLevel.BASIC
    
    def _generate_recommendations(self, violations: List[str], schema: RepositorySchema) -> List[str]:
        """Generate actionable recommendations based on violations"""
        recommendations = []
        
        # Group similar violations and provide solutions
        for violation in violations:
            if "Missing required directory" in violation:
                dir_name = violation.split(": ")[-1]
                recommendations.append(f"Create directory: mkdir -p {dir_name}")
            
            elif "Missing required file" in violation:
                file_name = violation.split(": ")[-1]
                recommendations.append(f"Create file: touch {file_name}")
            
            elif "README.md" in violation:
                recommendations.append("Improve README.md: Add title, description, and usage sections")
            
            elif "manifest" in violation:
                recommendations.append("Fix fcm.manifest.json: Ensure all required fields are present")
            
            elif "naming convention" in violation:
                recommendations.append("Fix naming: Use kebab-case for files, lowercase for directories")
        
        return list(set(recommendations))  # Remove duplicates


def main():
    """CLI interface for repository validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="FCM Repository Validator")
    parser.add_argument("repo_path", help="Path to repository to validate")
    parser.add_argument("--type", help="Repository type (auto-detected if not provided)")
    parser.add_argument("--schema", default="schemas/fcm-repository.json", help="Path to validation schema")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    validator = FCMRepositoryValidator(args.schema)
    result = validator.validate_repository(args.repo_path, args.type)
    
    if args.json:
        # JSON output for automation
        output = {
            "score": result.score,
            "compliance_level": result.compliance_level.name,
            "violations": result.violations,
            "recommendations": result.recommendations,
            "health_metrics": result.health_metrics
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable output
        print(f"Repository Validation Results")
        print(f"============================")
        print(f"Overall Score: {result.score:.2f}")
        print(f"Compliance Level: {result.compliance_level.name}")
        print()
        
        if result.violations:
            print("Violations:")
            for violation in result.violations:
                print(f"  ❌ {violation}")
            print()
        
        if result.recommendations:
            print("Recommendations:")
            for rec in result.recommendations:
                print(f"  💡 {rec}")
            print()
        
        print("Health Metrics:")
        for metric, value in result.health_metrics.items():
            print(f"  {metric}: {value:.2f}")


if __name__ == "__main__":
    main()
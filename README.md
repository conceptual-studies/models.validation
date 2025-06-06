# FCM Repository Validation Framework

Formal validation framework implementing the GitHub Repository Model for FCM repositories.

## System Overview

This validator implements all 6 layers of the formal GitHub Repository Model:

- **Layer 1 (Axioms)**: Structure/Validate/Enforce/Repository concepts
- **Layer 2 (Logic)**: Repository components and validation frameworks  
- **Layer 3 (Mathematics)**: Validation algorithms and scoring systems
- **Layer 4 (Mechanics)**: Git integration and enforcement mechanisms
- **Layer 5 (Reflection)**: Health monitoring and organizational intelligence
- **Layer 6 (Emergence)**: Transcendent organizational coherence

## Components

### 📋 Schemas (`schemas/`)
- `fcm-repository.json` - Complete validation schema with repository type definitions
- Compliance levels (0-5) from Basic to Exemplary
- Type-specific requirements for framework/systems/domains/works/projects/lab

### 🔍 Validators (`validators/`)
- `repo_validator.py` - Core validation engine implementing Layer 3 algorithms
- Structural, content, process, and security validation
- Auto-detection of repository types
- Comprehensive reporting with recommendations

### 🔗 Git Integration (`hooks/`)
- `pre-commit` - Git pre-commit hook for validation
- `github-workflow.yml` - Complete GitHub Actions workflow
- `install.sh` - One-command installation script
- Automated PR commenting and badge generation

### 📊 Monitoring (`monitoring/`)
- `compliance_scorer.py` - Advanced compliance scoring with trends
- `health_dashboard.py` - Organizational health monitoring with SQLite tracking
- Historical trend analysis and organizational recommendations

### 🔧 Remediation (`remediation/`)
- `auto_fix.py` - Automated fixing of common violations
- Safety levels (safe/caution/risky) with backup creation
- Template-based file generation
- Dry-run capability

## Installation

```bash
# Copy to your repository
cp -r repository-validator /path/to/your/repo/

# Install hooks and workflows
cd /path/to/your/repo
./repository-validator/hooks/install.sh
```

## Usage

### Manual Validation
```bash
# Validate current repository
python3 repository-validator/validators/repo_validator.py .

# Validate with specific type
python3 repository-validator/validators/repo_validator.py . --type framework

# JSON output for automation
python3 repository-validator/validators/repo_validator.py . --json
```

### Auto-Remediation
```bash
# Show what would be fixed (dry run)
python3 repository-validator/remediation/auto_fix.py . --dry-run

# Fix safe issues only
python3 repository-validator/remediation/auto_fix.py . --safe-only

# Fix with caution level
python3 repository-validator/remediation/auto_fix.py . --safety-level caution
```

### Health Monitoring
```bash
# Update health data
python3 repository-validator/monitoring/health_dashboard.py --action update --repo-name myrepo --validation-result result.json

# Generate dashboard
python3 repository-validator/monitoring/health_dashboard.py --action dashboard --format markdown

# Repository-specific report
python3 repository-validator/monitoring/health_dashboard.py --action repository --repo-name myrepo --days 30
```

## Validation Results

The validator provides comprehensive results including:

- **Overall Score** (0.0-1.0) with weighted category scoring
- **Compliance Level** (Basic → Structured → Documented → Tested → Secure → Exemplary)
- **Health Grade** (A+ to F) based on overall performance
- **Category Breakdown** (Structural, Content, Process, Security, Evolution)
- **Specific Violations** with actionable remediation suggestions
- **Trend Analysis** (improving/stable/declining)

## FCM Repository Types

### Framework (`framework`)
- **Required**: `core/`, `composite/`, `bridges/`, `templates/`
- **Focus**: Pure framework patterns, no implementations
- **Example**: models.core

### Systems (`systems`) 
- **Required**: `analytical/`, `empirical/`, `exports/`
- **Focus**: Working system implementations with CMI
- **Example**: models.systems

### Domains (`domains`)
- **Required**: `models/`, `schemas/`
- **Focus**: Domain-specific model collections
- **Example**: models.physics

### Works (`works`)
- **Required**: `formal/`, `informal/`, `transformations/`
- **Focus**: Complete books/papers with transformation tracking

### Projects (`projects`)
- **Required**: `models/`, `implementations/`, `case-studies/`
- **Focus**: Applied projects using multiple FCM repos

### Lab (`lab`)
- **Required**: `experiments/`, `proposals/`
- **Focus**: Experimental work with graduation criteria

## Compliance Levels

- **Level 0 (Basic)**: README and LICENSE exist
- **Level 1 (Structured)**: Proper directory hierarchy
- **Level 2 (Documented)**: Complete documentation
- **Level 3 (Tested)**: Validation and testing present
- **Level 4 (Secure)**: Security policies implemented  
- **Level 5 (Exemplary)**: Organizational best practices

## Integration

### Git Hooks
- Pre-commit validation with configurable score thresholds
- Automatic remediation suggestions
- Bypass option for emergencies (`git commit --no-verify`)

### GitHub Actions
- Full validation on push/PR
- Automated PR commenting with results
- Weekly health checks
- Compliance badge generation
- Security scanning integration

### Monitoring
- SQLite database for health tracking
- Historical trend analysis
- Organization-wide dashboard
- Critical issue alerting

## Configuration

### Validation Schema
Edit `schemas/fcm-repository.json` to customize:
- Required directories/files per repository type
- Naming conventions
- Content requirements
- Compliance thresholds

### Hook Configuration
Edit `.git/hooks/pre-commit` to adjust:
- Minimum score requirements
- Blocking vs warning mode
- Auto-remediation settings

## Layer 6 Capabilities

The system demonstrates transcendent organizational capabilities:

- **Organizational Coherence**: Consistent patterns across all repositories
- **Collective Intelligence**: Learning from repository analysis patterns
- **Adaptive Standards**: Standards that evolve based on effectiveness metrics
- **Cultural Manifestation**: Repository structures expressing organizational values

## Testing

Validated against:
- ✅ models.core (framework type)
- ✅ models.systems (systems type) 
- ✅ Various compliance scenarios
- ✅ Git integration workflows
- ✅ Remediation safety levels

## Architecture

The validator embodies the formal model it implements:
- **Self-Contained**: Complete validation system
- **Progressive Definition**: Each layer builds on previous
- **Universal Pattern**: Six-layer structure throughout
- **Git Layer Operation**: Seamless integration with development workflow

This implementation transforms repository management from manual oversight to systematic, self-enforcing organizational architecture.
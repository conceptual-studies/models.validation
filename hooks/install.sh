#!/bin/bash
#
# FCM Repository Validator Installation Script
# Sets up Git hooks and GitHub Actions workflow
#

set -e

echo "🚀 Installing FCM Repository Validator"
echo "======================================"

# Get repository root
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
VALIDATOR_DIR="$REPO_ROOT/repository-validator"

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "❌ Not in a Git repository"
    exit 1
fi

# Check if validator directory exists
if [ ! -d "$VALIDATOR_DIR" ]; then
    echo "❌ Validator directory not found: $VALIDATOR_DIR"
    echo "💡 Make sure you're running this from a repository with repository-validator/"
    exit 1
fi

echo "📁 Repository root: $REPO_ROOT"
echo "🔧 Validator directory: $VALIDATOR_DIR"

# Install Git hooks
echo ""
echo "📋 Installing Git hooks..."

# Create hooks directory if it doesn't exist
mkdir -p "$REPO_ROOT/.git/hooks"

# Install pre-commit hook
cp "$VALIDATOR_DIR/hooks/pre-commit" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
echo "✅ Pre-commit hook installed"

# Install GitHub Actions workflow
echo ""
echo "📋 Installing GitHub Actions workflow..."

mkdir -p "$REPO_ROOT/.github/workflows"
cp "$VALIDATOR_DIR/hooks/github-workflow.yml" "$REPO_ROOT/.github/workflows/fcm-validation.yml"
echo "✅ GitHub Actions workflow installed"

# Install Python dependencies
echo ""
echo "📋 Installing Python dependencies..."

if command -v python3 >/dev/null 2>&1; then
    python3 -m pip install --user jsonschema pyyaml > /dev/null 2>&1 || {
        echo "⚠️  Could not install Python dependencies automatically"
        echo "💡 Install manually: pip install jsonschema pyyaml"
    }
    echo "✅ Python dependencies installed"
else
    echo "⚠️  Python 3 not found - install it for full functionality"
fi

# Make validator executable
chmod +x "$VALIDATOR_DIR/validators/repo_validator.py"

# Run initial validation
echo ""
echo "📋 Running initial validation..."
echo ""

if python3 "$VALIDATOR_DIR/validators/repo_validator.py" "$REPO_ROOT"; then
    echo ""
    echo "🎉 Installation completed successfully!"
else
    echo ""
    echo "⚠️  Installation completed but repository has validation issues"
    echo "💡 Check the violations above and fix them for better compliance"
fi

echo ""
echo "📖 Usage:"
echo "  • Validation runs automatically on git commit"
echo "  • Manual validation: python3 repository-validator/validators/repo_validator.py ."
echo "  • GitHub Actions runs on push/PR"
echo "  • Bypass validation: git commit --no-verify (not recommended)"
echo ""
echo "🔧 Configuration:"
echo "  • Edit repository-validator/schemas/fcm-repository.json for custom rules"
echo "  • Modify .git/hooks/pre-commit for different score thresholds"
echo ""

exit 0
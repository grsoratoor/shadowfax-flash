#!/bin/bash
# Script to deploy shadowfax-flash to PyPI

set -e  # Exit on error

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "Error: This script must be run from the project root directory"
    exit 1
fi

# Check for required commands
for cmd in python3 twine; do
    if ! command -v $cmd &> /dev/null; then
        echo "Error: $cmd is required but not installed"
        exit 1
    fi
done

# Get version from pyproject.toml
VERSION=$(grep '^version = "[0-9]\+\.[0-9]\+\.[0-9]\+"' pyproject.toml | cut -d'"' -f2)
if [ -z "$VERSION" ]; then
    echo "Error: Could not extract version from pyproject.toml"
    exit 1
fi

echo "🚀 Preparing to deploy shadowfax-flash v$VERSION to PyPI"
echo "========================================"

# Clean up previous builds
echo "🧹 Cleaning up previous builds..."
rm -rf dist/ build/ *.egg-info

# Install build dependencies
echo "📦 Installing build dependencies..."
pip install --upgrade build twine

# Build the package
echo "🔨 Building package..."
python -m build

# Verify the built package
echo "🔍 Verifying package..."
twine check dist/*

# Ask for confirmation before uploading
read -p "⚠️  Ready to upload to PyPI? [y/N] " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "🚫 Upload cancelled"
    exit 0
fi

# Upload to PyPI
echo "🚀 Uploading to PyPI..."
twine upload dist/*

echo "✅ Successfully deployed shadowfax-flash v$VERSION to PyPI!"
echo "   You can install it with: pip install shadowfax-flash==$VERSION"

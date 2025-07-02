#!/usr/bin/env python3
"""
Deployment script for shadowfax-flash package.

This script automates the process of building and uploading the package to PyPI.
"""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional

def run_command(cmd: list[str], cwd: Optional[Path] = None) -> None:
    """Run a shell command and exit on failure."""
    print(f"🚀 Running: {' '.join(cmd)}")
    try:
        subprocess.run(cmd, check=True, cwd=cwd)
    except subprocess.CalledProcessError as e:
        print(f"❌ Command failed with exit code {e.returncode}")
        sys.exit(1)

def get_version() -> str:
    """Extract version from pyproject.toml."""
    with open("pyproject.toml", "r") as f:
        content = f.read()
    
    match = re.search(r'^version\s*=\s*"([\d.]+)"', content, re.MULTILINE)
    if not match:
        print("❌ Could not extract version from pyproject.toml")
        sys.exit(1)
    
    version = match.group(1)
    print(f"📦 Found version: {version}")
    return version

def clean_build() -> None:
    """Clean up build artifacts."""
    print("🧹 Cleaning up previous builds...")
    build_dirs = ["dist", "build", "*.egg-info"]
    for d in build_dirs:
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)

def install_build_deps() -> None:
    """Install build dependencies."""
    print("📦 Installing build dependencies...")
    run_command([sys.executable, "-m", "pip", "install", "--upgrade", "build", "twine"])

def build_package() -> None:
    """Build the package."""
    print("🔨 Building package...")
    run_command([sys.executable, "-m", "build"])

def verify_package() -> None:
    """Verify the built package."""
    print("🔍 Verifying package...")
    run_command(["twine", "check", "dist/*"])

def upload_to_pypi() -> None:
    """Upload the package to PyPI."""
    print("🚀 Uploading to PyPI...")
    run_command(["twine", "upload", "dist/*"])

def confirm_upload(version: str) -> bool:
    """Ask for confirmation before uploading."""
    print(f"\n🚀 Ready to upload shadowfax-flash v{version} to PyPI")
    print("=" * 50)
    print("\033[93m⚠️  WARNING: This will make the package publicly available on PyPI.\033[0m")
    response = input("\nContinue? [y/N]: ").strip().lower()
    return response in ('y', 'yes')

def main() -> None:
    # Check if we're in the project root
    if not os.path.exists("pyproject.toml"):
        print("❌ Error: This script must be run from the project root directory")
        sys.exit(1)

    # Get version
    version = get_version()
    
    # Clean up
    clean_build()
    
    # Install build dependencies
    install_build_deps()
    
    # Build the package
    build_package()
    
    # Verify the package
    verify_package()
    
    # Confirm before uploading
    if not confirm_upload(version):
        print("\n🚫 Upload cancelled")
        return
    
    # Upload to PyPI
    upload_to_pypi()
    
    print(f"\n✅ Successfully deployed shadowfax-flash v{version} to PyPI!")
    print(f"   You can install it with: pip install shadowfax-flash=={version}")

if __name__ == "__main__":
    main()

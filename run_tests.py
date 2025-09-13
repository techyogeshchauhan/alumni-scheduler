#!/usr/bin/env python3
"""
Test runner for Alumni Event Scheduler
Runs all tests and generates coverage reports
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path

def run_command(command, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print("Error:", e.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Run tests for Alumni Event Scheduler')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--e2e', action='store_true', help='Run only end-to-end tests')
    
    args = parser.parse_args()
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    print("🧪 Alumni Event Scheduler Test Suite")
    print("=" * 60)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected")
        print("   Consider activating your virtual environment first")
    
    # Install test dependencies
    if not run_command("pip install pytest pytest-cov pytest-mock", "Installing test dependencies"):
        print("❌ Failed to install test dependencies")
        return 1
    
    # Run linting
    print("\n🔍 Running code quality checks...")
    if not run_command("python -m flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics", "Running flake8 linting"):
        print("⚠️  Linting issues found, but continuing with tests")
    
    # Run tests
    test_commands = []
    
    if args.unit or not any([args.integration, args.e2e]):
        test_commands.append(("python -m pytest test_api.py -v", "Unit Tests"))
    
    if args.integration or not any([args.unit, args.e2e]):
        test_commands.append(("python -m pytest tests/integration/ -v", "Integration Tests"))
    
    if args.e2e or not any([args.unit, args.integration]):
        test_commands.append(("python -m pytest tests/e2e/ -v", "End-to-End Tests"))
    
    if not test_commands:
        test_commands.append(("python -m pytest test_api.py -v", "All Tests"))
    
    # Add coverage if requested
    if args.coverage:
        for i, (cmd, desc) in enumerate(test_commands):
            test_commands[i] = (f"{cmd} --cov=. --cov-report=html --cov-report=term", desc)
    
    # Run all test commands
    all_passed = True
    for command, description in test_commands:
        if not run_command(command, description):
            all_passed = False
    
    # Generate coverage report
    if args.coverage and all_passed:
        print("\n📊 Coverage Report Generated")
        print("   Open htmlcov/index.html in your browser to view detailed coverage")
    
    # Summary
    print("\n" + "="*60)
    if all_passed:
        print("🎉 All tests passed successfully!")
        return 0
    else:
        print("❌ Some tests failed. Please check the output above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

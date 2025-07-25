#!/usr/bin/env python3
"""
Test runner script for Signal Protocol implementation.

This script runs all tests in the organized test structure.
"""

import sys
import os
import unittest
import subprocess

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def run_test_file(test_file_path):
    """Run a single test file using subprocess with proper PYTHONPATH"""
    env = os.environ.copy()
    env['PYTHONPATH'] = project_root

    cmd = [sys.executable, test_file_path]
    result = subprocess.run(cmd, env=env, capture_output=True, text=True)

    print(f"Running {test_file_path}:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)

    return result.returncode == 0


def find_all_test_files():
    """Find all test files in the tests directory"""
    test_files = []
    tests_dir = os.path.join(project_root, 'tests')

    for root, dirs, files in os.walk(tests_dir):
        for file in files:
            if file.startswith('test_') and file.endswith('.py'):
                test_files.append(os.path.join(root, file))

    return test_files


def run_all_tests():
    """Run all tests in the project"""
    test_files = find_all_test_files()

    print(f"Found {len(test_files)} test files:")
    for test_file in test_files:
        print(f"  - {os.path.relpath(test_file, project_root)}")
    print()

    all_passed = True
    for test_file in test_files:
        success = run_test_file(test_file)
        if not success:
            all_passed = False
        print("-" * 70)

    return all_passed


if __name__ == '__main__':
    success = run_all_tests()

    if success:
        print("🎉 All tests passed!")
    else:
        print("❌ Some tests failed!")

    sys.exit(0 if success else 1)

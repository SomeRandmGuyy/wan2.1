#!/usr/bin/env python3
"""
Simple validation script for Grok I2V integration
This script validates the code structure without requiring dependencies.
"""

import os
import re

def check_file_exists(filepath, description):
    """Check if a file exists."""
    if os.path.exists(filepath):
        print(f"✓ {description}: {filepath}")
        return True
    else:
        print(f"✗ {description} not found: {filepath}")
        return False

def check_file_contains(filepath, patterns, description):
    """Check if a file contains certain patterns."""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        
        found_all = True
        for pattern in patterns:
            if isinstance(pattern, str):
                if pattern in content:
                    print(f"  ✓ Contains: {pattern[:50]}")
                else:
                    print(f"  ✗ Missing: {pattern[:50]}")
                    found_all = False
            else:  # regex pattern
                if pattern.search(content):
                    print(f"  ✓ Matches pattern: {pattern.pattern[:50]}")
                else:
                    print(f"  ✗ Pattern not found: {pattern.pattern[:50]}")
                    found_all = False
        
        if found_all:
            print(f"✓ {description}")
        else:
            print(f"✗ {description} - some patterns missing")
        
        return found_all
    except Exception as e:
        print(f"✗ Error checking {description}: {e}")
        return False

def main():
    """Run validation checks."""
    print("=" * 60)
    print("Grok I2V Integration Validation")
    print("=" * 60)
    print()
    
    results = []
    
    # Check main files exist
    print("1. Checking file structure...")
    results.append(check_file_exists('wan/grok_i2v.py', 'Grok I2V module'))
    results.append(check_file_exists('GROK_INTEGRATION.md', 'Integration documentation'))
    print()
    
    # Check GrokI2V class
    print("2. Validating wan/grok_i2v.py...")
    results.append(check_file_contains('wan/grok_i2v.py', [
        'class GrokI2V',
        'def generate(',
        'XAI_API_KEY',
        'requests.post',
    ], 'GrokI2V class structure'))
    print()
    
    # Check wan/__init__.py
    print("3. Validating wan/__init__.py...")
    results.append(check_file_contains('wan/__init__.py', [
        'from .grok_i2v import GrokI2V',
    ], 'GrokI2V import in wan/__init__.py'))
    print()
    
    # Check config integration
    print("4. Validating wan/configs/__init__.py...")
    results.append(check_file_contains('wan/configs/__init__.py', [
        'grok_i2v',
        "'grok-i2v': grok_i2v",
        "'grok-i2v': ('720*1280'",
    ], 'grok-i2v config registration'))
    print()
    
    # Check generate.py integration
    print("5. Validating generate.py...")
    results.append(check_file_contains('generate.py', [
        '"grok-i2v"',
        re.compile(r'elif\s+"grok-i2v"\s+in\s+args\.task'),
        'wan.GrokI2V',
        'grok_i2v.generate',
    ], 'grok-i2v task in generate.py'))
    print()
    
    # Check requirements.txt
    print("6. Validating requirements.txt...")
    results.append(check_file_contains('requirements.txt', [
        'requests',
    ], 'requests dependency'))
    print()
    
    # Check README.md
    print("7. Validating README.md...")
    results.append(check_file_contains('README.md', [
        'Grok API',
        'XAI_API_KEY',
        'GROK_INTEGRATION.md',
    ], 'Grok integration mentioned in README'))
    print()
    
    # Summary
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Validation Results: {passed}/{total} checks passed")
    print()
    
    if passed == total:
        print("✓ All validation checks passed!")
        print("\nThe Grok I2V integration is properly structured.")
        print("To use it:")
        print("  1. Set XAI_API_KEY environment variable")
        print("  2. Run: python generate.py --task grok-i2v --image <image_path>")
        return 0
    else:
        print("✗ Some validation checks failed")
        return 1

if __name__ == '__main__':
    import sys
    sys.exit(main())

#!/usr/bin/env python3
"""
Test script for Grok I2V integration
This script demonstrates the usage pattern without making actual API calls.
"""

import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_grok_i2v_import():
    """Test that the GrokI2V class can be imported."""
    print("Testing Grok I2V import...")
    try:
        from wan.grok_i2v import GrokI2V
        print("✓ Successfully imported GrokI2V class")
        return True
    except ImportError as e:
        print(f"✗ Failed to import GrokI2V: {e}")
        return False

def test_config_registration():
    """Test that grok-i2v task is registered in configs."""
    print("\nTesting config registration...")
    try:
        from wan.configs import WAN_CONFIGS, SUPPORTED_SIZES
        
        if 'grok-i2v' in WAN_CONFIGS:
            print("✓ grok-i2v task registered in WAN_CONFIGS")
        else:
            print("✗ grok-i2v task not found in WAN_CONFIGS")
            return False
        
        if 'grok-i2v' in SUPPORTED_SIZES:
            print(f"✓ grok-i2v supported sizes: {SUPPORTED_SIZES['grok-i2v']}")
        else:
            print("✗ grok-i2v not found in SUPPORTED_SIZES")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Config test failed: {e}")
        return False

def test_api_key_validation():
    """Test API key validation."""
    print("\nTesting API key validation...")
    try:
        from wan.grok_i2v import GrokI2V
        
        # Should fail without API key
        os.environ.pop('XAI_API_KEY', None)
        try:
            client = GrokI2V()
            print("✗ Should have raised ValueError for missing API key")
            return False
        except ValueError as e:
            print(f"✓ Correctly raised ValueError: {str(e)[:50]}...")
        
        # Should succeed with API key
        os.environ['XAI_API_KEY'] = 'test_key'
        try:
            client = GrokI2V()
            print("✓ Successfully created client with API key")
        except Exception as e:
            print(f"✗ Failed to create client with API key: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"✗ API key validation test failed: {e}")
        return False

def test_example_prompts():
    """Test that example prompts are defined."""
    print("\nTesting example prompts...")
    try:
        # We need to mock torch to import generate module
        import unittest.mock as mock
        
        # Read generate.py and check for grok-i2v in EXAMPLE_PROMPT
        with open('generate.py', 'r') as f:
            content = f.read()
            if '"grok-i2v"' in content and 'EXAMPLE_PROMPT' in content:
                print("✓ grok-i2v example prompt found in generate.py")
                return True
            else:
                print("✗ grok-i2v example prompt not found")
                return False
    except Exception as e:
        print(f"✗ Example prompt test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Grok I2V Integration Test Suite")
    print("=" * 60)
    
    tests = [
        test_grok_i2v_import,
        test_config_registration,
        test_api_key_validation,
        test_example_prompts,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"\n✗ Test {test.__name__} raised exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Test Results: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())

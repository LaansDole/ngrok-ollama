#!/usr/bin/env python3
"""
Test runner for all UI tests
"""
import subprocess
import sys
import os

def run_test(test_name):
    """Run a specific test and return success status"""
    try:
        print(f"\n{'='*50}")
        print(f"Running {test_name}")
        print(f"{'='*50}")
        
        result = subprocess.run(
            [sys.executable, f"test/{test_name}"],
            cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED")
            return True
        else:
            print(f"❌ {test_name} FAILED (exit code: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"❌ {test_name} ERROR: {e}")
        return False

def main():
    """Run all tests"""
    tests = [
        "test_connection.py",
        "test_streamlit_connection.py", 
        "test_worker.py"
    ]
    
    print("Running all UI tests...")
    
    results = {}
    for test in tests:
        results[test] = run_test(test)
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(results.values())
    total = len(results)
    
    for test, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{test:<30} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("💥 Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()

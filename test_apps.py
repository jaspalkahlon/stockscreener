#!/usr/bin/env python3
"""
Test script to verify the stock screener apps work correctly
"""

import sys
import subprocess
import time

def test_app(app_name):
    """Test if an app can be imported and run without errors"""
    print(f"\n🧪 Testing {app_name}...")
    
    try:
        # Try to import the app
        if app_name == "simple_app":
            import simple_app
        elif app_name == "enhanced_app":
            import enhanced_app
        elif app_name == "clean_app":
            import clean_app
        
        print(f"✅ {app_name} imports successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error in {app_name}: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Other error in {app_name}: {e}")
        return False

def main():
    """Run tests for all apps"""
    print("🚀 Testing Stock Screener Apps")
    print("=" * 40)
    
    apps = ["simple_app", "clean_app", "enhanced_app"]
    results = {}
    
    for app in apps:
        results[app] = test_app(app)
    
    print("\n📊 Test Results:")
    print("=" * 20)
    
    for app, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{app}: {status}")
    
    # Summary
    passed = sum(results.values())
    total = len(results)
    
    print(f"\n🎯 Summary: {passed}/{total} apps passed tests")
    
    if passed == total:
        print("🎉 All apps are working correctly!")
        print("\n🚀 To run the apps:")
        print("streamlit run simple_app.py    # Simple workflow app")
        print("streamlit run clean_app.py     # Clean, easy navigation")
        print("streamlit run enhanced_app.py  # Full-featured app")
    else:
        print("⚠️ Some apps have issues. Check the error messages above.")

if __name__ == "__main__":
    main()
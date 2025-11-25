#!/usr/bin/env python3
"""
Test script for extract_and_match_usecase.py
Tests various use case inputs and verifies JSON output
"""
import json
import sys
from extract_and_match_usecase import extract_and_match_usecase

def test_usecase(input_text: str, expected_fields: list = None, description: str = ""):
    """Test a use case input and verify output"""
    print("=" * 70)
    if description:
        print(f"Test: {description}")
    print(f"Input: {input_text}")
    print("-" * 70)
    
    try:
        result = extract_and_match_usecase(input_text)
        
        print("\nOutput JSON:")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        # Verify required fields
        assert "use_case" in result, "Missing required field: use_case"
        print("\n✓ Required field 'use_case' present")
        
        # Verify expected fields
        if expected_fields:
            for field in expected_fields:
                if field in result:
                    print(f"✓ Expected field '{field}' present: {result[field]}")
                else:
                    print(f"⚠ Expected field '{field}' not found (may be optional)")
        
        # Verify no unexpected fields
        allowed_fields = ["use_case", "user_count", "priority", "hardware"]
        unexpected = [k for k in result.keys() if k not in allowed_fields]
        if unexpected:
            print(f"⚠ Unexpected fields found: {unexpected}")
        else:
            print("✓ No unexpected fields")
        
        return result
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    print("=" * 70)
    print("  Testing Use Case Extraction & Matching")
    print("=" * 70)
    print()
    
    # Test cases
    test_cases = [
        {
            "input": "I need a chatbot for 100 users with high priority",
            "expected": ["use_case", "user_count", "priority"],
            "description": "Full information: chatbot, users, priority"
        },
        {
            "input": "I need code autocomplete for my IDE, needs GPU",
            "expected": ["use_case", "hardware"],
            "description": "Code completion with hardware requirement"
        },
        {
            "input": "I need a math problem solver for 50 employees",
            "expected": ["use_case", "user_count"],
            "description": "Math solver with user count"
        },
        {
            "input": "I need document summarization",
            "expected": ["use_case"],
            "description": "Minimal input: only use case"
        },
        {
            "input": "I need a QA medical expert for 200 users, urgent, needs cloud infrastructure",
            "expected": ["use_case", "user_count", "priority", "hardware"],
            "description": "Custom use case with all optional fields"
        },
        {
            "input": "I need translation service for 500 customers, medium priority",
            "expected": ["use_case", "user_count", "priority"],
            "description": "Translation with users and priority"
        },
        {
            "input": "I need a financial analysis tool",
            "expected": ["use_case"],
            "description": "Custom use case (no match to predefined)"
        },
        {
            "input": "I need content generation for 10 team members, low priority, needs server",
            "expected": ["use_case", "user_count", "priority", "hardware"],
            "description": "Content generation with all fields"
        },
    ]
    
    results = []
    passed = 0
    failed = 0
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n\n{'='*70}")
        print(f"TEST CASE {i}/{len(test_cases)}")
        print('='*70)
        
        result = test_usecase(
            test_case["input"],
            test_case.get("expected", []),
            test_case.get("description", "")
        )
        
        if result:
            results.append(result)
            passed += 1
            print("\n✓ Test PASSED")
        else:
            failed += 1
            print("\n✗ Test FAILED")
    
    # Summary
    print("\n\n" + "=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(test_cases)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 70)
    
    # Save all results to JSON file
    output_file = "test_usecase_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_cases": test_cases,
            "results": results,
            "summary": {
                "total": len(test_cases),
                "passed": passed,
                "failed": failed
            }
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ All test results saved to {output_file}")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


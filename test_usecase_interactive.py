#!/usr/bin/env python3
"""
Interactive test for use case extraction
Type a use case and see the JSON output
"""
import json
import sys
from extract_and_match_usecase import extract_and_match_usecase

def main():
    print("=" * 70)
    print("  Interactive Use Case Extraction Test")
    print("=" * 70)
    print("\nType your use case description (or 'quit' to exit)")
    print("Examples:")
    print("  - I need a chatbot for 100 users with high priority")
    print("  - I need code autocomplete for my IDE, needs GPU")
    print("  - I need a math problem solver")
    print("-" * 70)
    
    while True:
        try:
            user_input = input("\n> ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\nGoodbye!")
                break
            
            if not user_input:
                print("Please enter some text.")
                continue
            
            print("\n" + "=" * 70)
            print("  Processing...")
            print("=" * 70)
            
            # Extract and match
            result = extract_and_match_usecase(user_input)
            
            # Display JSON
            print("\n" + "=" * 70)
            print("  JSON OUTPUT")
            print("=" * 70)
            print(json.dumps(result, indent=2, ensure_ascii=False))
            print("=" * 70)
            
            # Save to file
            output_file = "usecase_output.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Saved to {output_file}")
            print("-" * 70)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()

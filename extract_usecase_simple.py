#!/usr/bin/env python3
"""
Simple interactive version: User types plain text, gets JSON file
"""
import json
import sys
from extract_usecase_from_text import extract_usecase_json

def main():
    print("=" * 70)
    print("  Plain Text to JSON Converter")
    print("=" * 70)
    print("\nType your use case description (or 'quit' to exit):")
    print("Example: 'I need a chatbot for 100 users with high priority'")
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
            
            # Extract JSON
            result = extract_usecase_json(user_input)
            
            # Generate output filename
            output_file = "usecase_extracted.json"
            
            # Save to JSON file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2)
            
            # Display results
            print("\n" + "=" * 70)
            print("  EXTRACTED JSON")
            print("=" * 70)
            print(json.dumps(result, indent=2))
            print(f"\n✓ Saved to {output_file}")
            print("=" * 70)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()


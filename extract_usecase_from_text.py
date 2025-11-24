#!/usr/bin/env python3
"""
Extract use case information from plain text and return structured JSON
User types plain text, system extracts: use_case, user_count, priority, hardware
"""
import json
import re
import sys
import argparse
from typing import Dict, Optional

def extract_user_count(text: str) -> Optional[int]:
    """Extract user count from text"""
    text_lower = text.lower()
    
    # Patterns for user count
    patterns = [
        r'(\d+)\s*users?',
        r'for\s+(\d+)\s*users?',
        r'(\d+)\s*people',
        r'(\d+)\s*employees',
        r'(\d+)\s*team\s*members?',
        r'serving\s+(\d+)',
        r'(\d+)\s*end\s*users?',
        r'(\d+)\s*customers?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text_lower)
        if match:
            try:
                count = int(match.group(1))
                if 1 <= count <= 1000000:  # Reasonable range
                    return count
            except ValueError:
                continue
    
    # Check for words like "few", "many", "hundreds", "thousands"
    if re.search(r'\b(few|several|some)\b', text_lower):
        return None  # Indeterminate
    if re.search(r'\b(hundreds?|thousands?|millions?)\b', text_lower):
        return None  # Too vague
    
    return None

def extract_priority(text: str) -> Optional[str]:
    """Extract priority level from text"""
    text_lower = text.lower()
    
    # High priority indicators
    if any(word in text_lower for word in ['critical', 'urgent', 'high priority', 'important', 'asap', 'immediately']):
        return 'high'
    
    # Medium priority indicators
    if any(word in text_lower for word in ['medium', 'normal', 'standard', 'moderate']):
        return 'medium'
    
    # Low priority indicators
    if any(word in text_lower for word in ['low priority', 'low', 'nice to have', 'optional']):
        return 'low'
    
    return None

def extract_hardware(text: str) -> Optional[str]:
    """Extract hardware requirements from text"""
    text_lower = text.lower()
    
    # Hardware keywords
    hardware_keywords = {
        'gpu': ['gpu', 'graphics card', 'nvidia', 'cuda'],
        'cpu': ['cpu', 'processor', 'intel', 'amd'],
        'memory': ['ram', 'memory', 'gb ram', 'mb ram'],
        'cloud': ['cloud', 'aws', 'azure', 'gcp', 'google cloud'],
        'edge': ['edge', 'edge device', 'raspberry pi', 'embedded'],
        'mobile': ['mobile', 'phone', 'smartphone', 'ios', 'android'],
        'server': ['server', 'datacenter', 'on-premise', 'on premise'],
    }
    
    found_hardware = []
    for hw_type, keywords in hardware_keywords.items():
        if any(keyword in text_lower for keyword in keywords):
            found_hardware.append(hw_type)
    
    if found_hardware:
        return ', '.join(found_hardware)
    
    return None

def extract_use_case_description(text: str) -> str:
    """Extract the main use case description from text"""
    # Start with original text
    cleaned = text
    
    # Remove user count patterns (more carefully)
    cleaned = re.sub(r'\s+for\s+\d+\s+users?\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+\d+\s+users?\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+for\s+\d+\s+employees?\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+\d+\s+employees?\b', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\s+\d+\s+people\b', '', cleaned, flags=re.IGNORECASE)
    
    # Remove priority phrases (keep the sentence structure)
    priority_phrases = [
        r'\s+with\s+high\s+priority\b',
        r'\s+high\s+priority\b',
        r'\s+with\s+critical\s+priority\b',
        r'\s+critical\s+priority\b',
        r'\s+urgent\b',
        r'\s+asap\b',
        r'\s+with\s+low\s+priority\b',
        r'\s+low\s+priority\b',
    ]
    for phrase in priority_phrases:
        cleaned = re.sub(phrase, '', cleaned, flags=re.IGNORECASE)
    
    # Remove hardware phrases
    hardware_phrases = [
        r'\s+needs?\s+cloud\s+infrastructure\b',
        r'\s+needs?\s+cloud\b',
        r'\s+needs?\s+gpu\b',
        r'\s+needs?\s+cpu\b',
        r'\s+needs?\s+server\b',
        r'\s+with\s+gpu\b',
        r'\s+with\s+cloud\b',
    ]
    for phrase in hardware_phrases:
        cleaned = re.sub(phrase, '', cleaned, flags=re.IGNORECASE)
    
    # Clean up extra spaces and punctuation
    cleaned = re.sub(r'\s+', ' ', cleaned)  # Multiple spaces to single
    cleaned = re.sub(r'\s*,\s*,', ',', cleaned)  # Double commas
    cleaned = cleaned.strip(' ,')
    
    # If cleaned is too short or doesn't make sense, use original
    if len(cleaned) < 10 or not cleaned:
        cleaned = text
    
    return cleaned.strip()

def extract_usecase_json(user_text: str) -> Dict:
    """
    Extract structured JSON from plain text user input
    
    Args:
        user_text: Plain text description from user
    
    Returns:
        Dictionary with use_case, user_count, priority, hardware
    """
    result = {
        "use_case": extract_use_case_description(user_text),
        "user_count": extract_user_count(user_text),
        "priority": extract_priority(user_text),
        "hardware": extract_hardware(user_text)
    }
    
    # Remove None values (optional fields)
    result = {k: v for k, v in result.items() if v is not None}
    
    return result

def main():
    parser = argparse.ArgumentParser(
        description='Extract use case JSON from plain text input',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 extract_usecase_from_text.py --text "I need a chatbot for 100 users with high priority"
  python3 extract_usecase_from_text.py --text "I need code autocomplete for my IDE, needs GPU"
  python3 extract_usecase_from_text.py --file input.txt --output output.json

Input: Plain text (e.g., "I need a math solver for 50 users, high priority, needs cloud")
Output: JSON with use_case, user_count, priority, hardware
        """
    )
    parser.add_argument('--text', '-t', type=str, help='Plain text input')
    parser.add_argument('--file', '-f', type=str, help='File with plain text input')
    parser.add_argument('--output', '-o', type=str, help='Output JSON file (optional)')
    
    args = parser.parse_args()
    
    if not args.text and not args.file:
        parser.print_help()
        sys.exit(1)
    
    # Get input text
    if args.text:
        user_text = args.text
    elif args.file:
        with open(args.file, 'r', encoding='utf-8') as f:
            user_text = f.read().strip()
    
    print("=" * 70)
    print("  Use Case Extraction from Plain Text")
    print("=" * 70)
    print(f"\n📝 Input Text: {user_text}")
    
    # Extract structured data
    print("\n🔍 Extracting information...")
    result = extract_usecase_json(user_text)
    
    # Display results
    print("\n" + "=" * 70)
    print("  EXTRACTED JSON")
    print("=" * 70)
    print(json.dumps(result, indent=2))
    
    # Save if output file specified
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
        print(f"\n✓ Saved to {args.output}")
    else:
        print("\n💡 Tip: Use --output filename.json to save")
    
    return result

if __name__ == "__main__":
    main()


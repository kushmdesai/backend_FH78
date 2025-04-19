import os
import json
import re

def pathgetter(filename):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, 'backend_api', filename)

def reader(path):
    with open(path, mode='r') as f:
        return f.read()

def writer(path, text):
    try:
    # Try to parse, assuming it's JSON
        parsed = json.loads(text)
        with open(path, mode='w') as f:
            json.dump(parsed, f, indent=2)
        print("✅ Saved valid JSON to file.")
    except json.JSONDecodeError:
        # If not JSON, save as plain text
        with open(path, mode='w') as f:
            f.write(text)
        print("⚠️ Saved raw text (not JSON).")

def validate_json(text):
    try:
        json.loads(text)  # Try parsing the string as JSON
        print("✅ JSON is valid!")
        return True
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed: {e}")
        return False


def editor_response():
    print("Starting...")
    path = pathgetter('response.txt')
    text = reader(path)

    print("Cleaning AI markup...")
    cleaned_text = re.sub(r'^```json\s*', '', text)
    cleaned_text = re.sub(r'\s*```$', '', cleaned_text).strip()

    try:
        parsed = json.loads(cleaned_text)  # Validate
        writer(path, json.dumps(parsed, indent=2, ensure_ascii=False))  # Re-save properly
        print("✅ JSON is valid and file updated successfully.")
    except json.JSONDecodeError as e:
        print(f"❌ JSON validation failed after cleaning: {e}")
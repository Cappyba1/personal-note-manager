import os
from datetime import datetime, timedelta

NOTES_DIR = os.path.join(os.path.dirname(__file__), "..", "Notes")

def find_notes_to_review(age_days=30):
    for file in os.listdir(NOTES_DIR):
        if file.endswith(".md"):
            with open(os.path.join(NOTES_DIR, file), "r") as f:
                content = f.read()
                metadata = extract_metadata(conten)
                if not metadata.get("tags") or metadata["tags"] == "None":
                    print(f"Untagged: {metadata.get('title', file)}")
                date_str = metadata.get("date")
                if date_str:
                    note_date = datetime.strptime(date_str, "%Y-%m-%d")
                    if datetime.now() - note_date > timedelta(days=age_days):
                        print(f"Old note: {metadata.get('title', file)}")

def extract_metadata(content):
    lines = content.split("\n")
    metadata = {}
    if lines[0] == "---":
        i = 1
        while i < len(lines) and lines[i] != "---":
            key, value = lines[i].split(": ", 1)
            metadata[key] = value
            i += 1
    return metadata

if __name__ == "__main__":
    find_notes_to_review()
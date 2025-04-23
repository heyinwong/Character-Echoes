import os

def list_plays():
    files = [f.replace(".txt", "") for f in os.listdir("data") if f.endswith(".txt")]
    cleaned = []

    for name in files:
        if name.lower() == "complete":
            cleaned.append("Complete Works (All Plays)")
        else:
            cleaned.append(name)

    cleaned = sorted(cleaned, key=lambda x: "complete works" not in x.lower())
    return cleaned

def load_play(play_name, data_dir="data"):
    if "complete works" in play_name.lower():
        play_name = "Complete"

    file_path = os.path.join(data_dir, f"{play_name}.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def search_quotes(play_text, keyword, max_results=3):
    import re
    lines = play_text.splitlines()
    keyword = keyword.lower()

    matches = [line.strip() for line in lines if keyword in line.lower() and line.strip()]
    return matches[:max_results]
import os

# List all play names from the source folder
def list_plays():
    path = "data/source"
    files = [f.replace(".txt", "") for f in os.listdir(path) if f.endswith(".txt")]
    cleaned = []

    for name in files:
        if name.lower() == "complete":
            cleaned.append("Complete Works (All Plays)")
        else:
            cleaned.append(name)

    cleaned = sorted(cleaned, key=lambda x: "complete works" not in x.lower())
    return cleaned

# Load play content
def load_play(play_name, data_dir="data/source"):
    if "complete works" in play_name.lower():
        play_name = "Complete"
    file_path = os.path.join(data_dir, f"{play_name}.txt")
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# Search relevant lines from play
def search_quotes(play_text, keyword, max_results=3):
    import re
    lines = play_text.splitlines()
    keyword = keyword.lower()
    matches = [line.strip() for line in lines if keyword in line.lower() and line.strip()]
    return matches[:max_results]

# List all character prompt names (markdown files)
def list_characters():
    folder = "data/character_prompts"
    files = [f for f in os.listdir(folder) if f.endswith(".md") and f != "default.md"]
    return sorted([f.replace(".md", "").replace("_", " ").title() for f in files])

# Load character prompt content
def load_prompt(character_name):
    character_file = character_name.lower().replace(" ", "_") + ".md"
    prompt_path = os.path.join("data/character_prompts", character_file)
    default_path = os.path.join("data/character_prompts", "default.md")

    def parse_prompt(path):
        prompt, suggest = "", ""
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("prompt:"):
                    prompt = line.replace("prompt:", "").strip()
                elif line.startswith("suggest:"):
                    suggest = line.replace("suggest:", "").strip()
        return prompt, suggest

    if os.path.exists(prompt_path):
        return parse_prompt(prompt_path)
    else:
        return parse_prompt(default_path)
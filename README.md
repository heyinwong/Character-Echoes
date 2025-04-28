# Echoes of Legends

**Echoes of Legends** is an AI-powered roleplay companion that allows users to interact with historical and fictional characters in an immersive conversational experience.

This project is an MVP to showcase the potential for educational tools, interactive storytelling, and creative exploration through AI-driven dialogue.

---

## Features

- **Roleplay with Shakespearean Characters**  
  Talk to Hamlet, Lady Macbeth, Juliet, Romeo, and more, each with their own unique speaking style and knowledge drawn from Shakespeare’s works.

- **Custom Character Roleplay**  
  Enter any character name appeared in Shakespearea's novels, and the AI will simulate that personality.

- **Upload Your Own Story**  
  Upload a `.txt` file of your own writing (or other historical fiction), and create characters based on it! The AI's responses will be based solely on the uploaded content.

- **Modern English or Bard Style**  
  Choose whether you want conversations in poetic Shakespearean English or simple modern English.

- **Quote Search Engine**  
  When you ask questions, the AI also retrieves relevant quotes or passages from the selected play or book to enrich the conversation.

---

## Example Use Cases

- "Summarize Act 3 Scene 1 of Macbeth in modern English."
- "Hamlet, what do you think about fate?"
- "Juliet, would you still love Romeo in today's world?"
- "Talk to a custom character from my own novel."

---

## Vision

This project proves the idea that **literary or historical character simulations** can be valuable tools for:

- Language learning and literary appreciation
- Interactive storytelling and writing aids
- Historical education and teaching
- Role-playing games and immersive experiences

The goal is to extend this approach beyond Shakespeare to other famous works, mythologies, or even user-generated worlds.

---

## Project Structure

```
├── app.py                 # Main Streamlit frontend
├── core/
│   ├── loader.py           # Load text files, search quotes, and manage uploads
│   └── responder.py        # OpenAI API handling
├── utils/
│   └── styles.py           # Custom CSS injection
├── data/
│   ├── source/             # Shakespearean plays and user-uploaded works
│   └── character_prompts/  # Character instruction files (.md)
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup (Local)

1. Set your OpenAI API Key (either via environment variable or Streamlit Secrets):

```bash
export OPENAI_API_KEY=your-api-key
```

2. Run the app locally:

```bash
streamlit run app.py
```

---

## Deployment

- Can be deployed easily on **Streamlit Cloud** or **Hugging Face Spaces** or any choice, just need to modify some of the code.
- Remember to safely configure your API Key via secret management tools.

---

## Attribution

- Shakespeare texts from [Project Gutenberg](https://www.gutenberg.org/)
- Built using [Streamlit](https://streamlit.io)
- Powered by [OpenAI API](https://platform.openai.com)

---

## Author

**Xixian Huang**  
for the [Microsoft AI Agent Hackathon](https://github.com/microsoft/AI_Agents_Hackathon)

---

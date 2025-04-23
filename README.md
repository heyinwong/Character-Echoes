# 🎭 Echoes of the Bard

**Echoes of the Bard** is a simple AI literature companion that lets you explore the works of William Shakespeare through natural language. This app can:

- Translate Shakespearean English into modern English or the other way round
- Roleplay as characters like Hamlet, Lady Macbeth, or Juliet
- Search and retrieve quotes from full-text Shakespeare plays
- Maintain an interactive chat with historical and literary style

---

## Example Questions

- "Summarize Act 1, Scene 3 of Macbeth in modern English."
- "What would Lady Macbeth say about ambition?"
- "Who said 'To be or not to be'?"
- "Translate this: 'Methinks the lady doth protest too much.'"

---

## Project Structure

```
├── app.py                 # Main Streamlit interface
├── core/
│   ├── loader.py         # Load + search Shakespeare text files
│   └── responder.py      # OpenAI response logic
├── utils/
│   └── styles.py         # Custom medieval CSS
├── data/                 # Plaintext Shakespeare plays (e.g. Macbeth.txt)
├── requirements.txt
└── README.md
```

---

## Setup (Local)

1. Clone the repo
2. Use your own API key and save it onto your environmental variable:

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the app:
```bash
streamlit run app.py
```

---

## Deployment

This app is ready to deploy on **Streamlit Cloud** or **Hugging Face Spaces**. Just add your API key as an environment variable or secret.

---

## Attribution

- Shakespeare texts from [Project Gutenberg](https://www.gutenberg.org/)
- Interface built with [Streamlit](https://streamlit.io)
- Powered by [OpenAI](https://platform.openai.com)

---

## Author
 **Xixian Huang**

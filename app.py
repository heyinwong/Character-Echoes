import streamlit as st
st.set_page_config(page_title="Echoes of Shakespeare", layout="centered")

import os
from dotenv import load_dotenv
from utils.styles import set_custom_style
from core.loader import list_plays, load_play, search_quotes
from core.responder import get_openai_response

# Load styles and environment variables
set_custom_style()
load_dotenv()

# Session state initialization
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "previous_character" not in st.session_state:
    st.session_state.previous_character = None

# Title
st.markdown("<h1 class='bard-title'>🎭 Echoes of Shakespeare</h1>", unsafe_allow_html=True)

# 📖 Play Selector
st.markdown("<div class='bard-label'>Choose a Shakespeare play:</div>", unsafe_allow_html=True)
plays = list_plays()
default_index = next((i for i, p in enumerate(plays) if "complete works" in p.lower()), 0)
selected_play = st.selectbox("Play Selector", plays, index=default_index, label_visibility="collapsed")
play_filename = "Complete" if "complete works" in selected_play.lower() else selected_play
play_text = load_play(play_filename)

# 🗣️ Language Style
st.markdown("<div class='bard-label'>Choose your language style:</div>", unsafe_allow_html=True)
mode = st.radio("", ["Modern English", "Bard Speak"], label_visibility="collapsed")

# 🎭 Mode Selector
st.markdown("<div class='bard-label'>Interaction Mode:</div>", unsafe_allow_html=True)
interaction_mode = st.radio("", ["Ask the Bard", "Roleplay Mode"], label_visibility="collapsed")

# 🎭 Character Selection
if interaction_mode == "Roleplay Mode":
    st.markdown("<div class='bard-label'>Choose a character to roleplay:</div>", unsafe_allow_html=True)
    character = st.selectbox("", ["Hamlet", "Lady Macbeth", "Romeo", "Juliet", "The Bard"], label_visibility="collapsed")

    # Clear chat history when character changes
    if st.session_state.previous_character and character != st.session_state.previous_character:
        st.session_state.chat_history = []
        st.info(f"Chat history cleared — now speaking with {character}.")
    st.session_state.previous_character = character
else:
    character = "Shakespeare"

# ✍️ User Input Label
input_label = f"Chat with {character}" if interaction_mode == "Roleplay Mode" else "Ask the Bard"
st.markdown(f"<div class='bard-label'>{input_label}</div>", unsafe_allow_html=True)
# 💡 Suggestions for user input
if interaction_mode == "Roleplay Mode":
    st.markdown(
        f"<div class='bard-suggestion'>You are now role-playing with {character}. Try something like:<br><em>“Hamlet, What do you think of fate?”</em></div>",
        unsafe_allow_html=True
    )
else:
    st.markdown(
        "<div class='bard-suggestion'>You can ask for summaries, scene explanations, or famous quotes.<br><em>e.g., 'Summarize Act 1 Scene 3 of Macbeth'</em></div>",
        unsafe_allow_html=True
    )
user_input = st.text_area("hidden-input", height=120, label_visibility="collapsed")

# 🔘 Buttons
col1, col2 = st.columns(2)
with col1:
    respond = st.button("Respond", use_container_width=True)
with col2:
    clear = st.button("Clear Chat", use_container_width=True)

# 🧹 Clear Chat
if clear:
    st.session_state.chat_history = []
    st.rerun()

# 💬 Generate Response
if respond and user_input.strip():
    messages = []

    # System prompt
    if interaction_mode == "Roleplay Mode":
        roles = {
            "Hamlet": "You are Prince Hamlet — philosophical, reflective, and deeply conflicted. Speak in a melancholic tone with poetic grace.",
            "Lady Macbeth": "You are Lady Macbeth — ambitious, persuasive, and intense. Speak with fiery passion and cunning resolve.",
            "Romeo": "You are Romeo Montague — romantic, impulsive, and dramatic. Speak with youthful passion and poetic language.",
            "Juliet": "You are Juliet Capulet — intelligent, bold, and eloquent. Speak with emotion and poetic expression.",
            "The Bard": "You are William Shakespeare — wise, witty, and poetic in all your responses."
        }
        persona = roles.get(character, "You are the Bard himself.")
        persona += " Use modern English." if mode == "Modern English" else " Speak in Shakespearean poetic style."
    else:
        persona = "You are the Bard himself. " + ("Explain clearly in modern English." if mode == "Modern English" else "Speak in poetic, Shakespearean language.")

    messages.append({"role": "system", "content": persona})

    # Add chat history
    for m in st.session_state.chat_history:
        messages.append({"role": "user" if m["role"] == "user" else "assistant", "content": m["text"]})

    # Relevant quotes
    matches = search_quotes(play_text, user_input)
    if matches:
        quote_context = "\n\n".join(matches)
        messages.append({"role": "system", "content": f"Relevant lines from the play:\n\n{quote_context}"})

    messages.append({"role": "user", "content": user_input})

    with st.spinner("Summoning the Bard..."):
        response = get_openai_response(messages)

    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bard", "text": response})

elif respond:
    st.warning("Please enter a message.")

# 🗨️ Chat History
convo_label = f"Conversation with {character}" if interaction_mode == "Roleplay Mode" else "Conversation with the Bard"
st.markdown(f"<div class='bard-label'>{convo_label}</div>", unsafe_allow_html=True)

for message in reversed(st.session_state.chat_history):
    if message["role"] == "user":
        st.markdown(f"""
            <div style='background-color: #ffffffdd; padding: 1rem; margin: 1rem 0; border-radius: 12px; text-align: right; color: #000; border: 1px solid #aaa; max-width: 80%; margin-left: auto;'>
                <strong>You:</strong><br>{message['text']}
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style='background-color: #f9f1e7; padding: 1rem; margin: 1rem 0; border-radius: 12px; color: #2b1d0e; border: 2px solid #c76b3e; max-width: 80%; margin-right: auto;'>
                <strong>{character}:</strong><br>{message['text']}
            </div>""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size: 0.85rem; margin-top: 2rem;'>"
    "Crafted with ☕ by <strong>Xixian Huang</strong>"
    "</div>",
    unsafe_allow_html=True
)

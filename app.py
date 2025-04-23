import streamlit as st
st.set_page_config(page_title="Echoes of Shakespeare", layout="centered")

import os
from dotenv import load_dotenv
from utils.styles import set_custom_style
from core.loader import list_plays, load_play, search_quotes, list_characters, load_prompt
from core.responder import get_openai_response

# Load styles and environment variables
set_custom_style()
load_dotenv()

# Session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "previous_character" not in st.session_state:
    st.session_state.previous_character = None
if "previous_mode" not in st.session_state:
    st.session_state.previous_mode = "Ask the Bard"

# Title
st.markdown("<h1 class='bard-title'>Echoes of Shakespeare</h1>", unsafe_allow_html=True)

# Interaction Mode
st.markdown("<div class='bard-label'>Choose mode:</div>", unsafe_allow_html=True)
interaction_mode = st.radio("Mode", ["Ask the Bard", "Roleplay"], label_visibility="collapsed")

# Clear chat if user switched interaction modes
if interaction_mode != st.session_state.previous_mode:
    st.session_state.chat_history = []
    st.info(f"Switched to {interaction_mode} mode. Chat history cleared.")
st.session_state.previous_mode = interaction_mode

# Ask the Bard mode
if interaction_mode == "Ask the Bard":
    st.markdown("<div class='bard-label'>Choose a Shakespeare play:</div>", unsafe_allow_html=True)
    plays = list_plays()
    default_index = next((i for i, p in enumerate(plays) if "complete works" in p.lower()), 0)
    selected_play = st.selectbox("Select a play", plays, index=default_index, label_visibility="collapsed")
    play_filename = "Complete" if "complete works" in selected_play.lower() else selected_play
    play_text = load_play(play_filename)
else:
    play_text = load_play("Complete")

# Language style
st.markdown("<div class='bard-label'>Choose your language style:</div>", unsafe_allow_html=True)
mode = st.radio("Language", ["Modern English", "Bard Speak"], label_visibility="collapsed")

# Roleplay characters
if interaction_mode == "Roleplay":
    st.markdown("<div class='bard-label'>Choose a character to roleplay:</div>", unsafe_allow_html=True)
    characters = list_characters()
    characters.append("Custom")
    character = st.selectbox("Choose a character", characters, index=0, label_visibility="collapsed")

    if character == "Custom":
        custom_character = st.text_input("Enter a custom character name:", label_visibility="collapsed")
        display_name = custom_character.strip() or "Someone You Desired"
    else:
        custom_character = ""
        display_name = character

    current_identity = custom_character if character == "Custom" else character
    if st.session_state.previous_character and current_identity != st.session_state.previous_character:
        st.session_state.chat_history = []
        st.info(f"Chat history cleared — now speaking with {display_name}.")
    st.session_state.previous_character = current_identity
else:
    character = "The Bard"
    display_name = character
    custom_character = ""

# Load prompt and suggestion
if interaction_mode == "Roleplay":
    instruction, suggestion = load_prompt(character if character != "Custom" else "default")
else:
    instruction = "You are a wise Shakespearean assistant. " + (
        "Explain clearly in modern English." if mode == "Modern English" else "Speak in poetic, Shakespearean language."
    )
    suggestion = "You can ask for summaries, scene explanations, or famous quotes. For example, 'Summarize Act 1 Scene 3 of Macbeth'."

# Input label
input_label = f"Chat with {display_name}" if interaction_mode == "Roleplay" else "Ask the Bard"
st.markdown(f"<div class='bard-label'>{input_label}</div>", unsafe_allow_html=True)

# Suggestion display
st.markdown(
    f"<div class='bard-suggestion'>Try asking {display_name} something like:<br><em>“{suggestion}”</em></div>",
    unsafe_allow_html=True
)

# Input
user_input = st.text_area("Your message", height=130, label_visibility="collapsed")

# Buttons
col1, col2 = st.columns(2)
with col1:
    respond = st.button("Respond", use_container_width=True)
with col2:
    clear = st.button("Clear Chat", use_container_width=True)

# Clear logic
if clear:
    st.session_state.chat_history = []
    st.rerun()

# Response generation
if respond and user_input.strip():
    persona = instruction + (" Use modern English." if mode == "Modern English" else " Speak in Shakespearean poetic style.")
    messages = [{"role": "system", "content": persona}]

    for m in st.session_state.chat_history:
        messages.append({"role": "user" if m["role"] == "user" else "assistant", "content": m["text"]})

    matches = search_quotes(play_text, user_input)
    if matches:
        quote_context = "\n\n".join(matches)
        messages.append({"role": "system", "content": f"Relevant lines from the play:\n\n{quote_context}"})

    messages.append({"role": "user", "content": user_input})

    with st.spinner("Summoning response..."):
        response = get_openai_response(messages)

    st.session_state.chat_history.append({"role": "user", "text": user_input})
    st.session_state.chat_history.append({"role": "bard", "text": response})

elif respond:
    st.warning("Please enter a message.")

# Chat history
convo_label = f"Conversation with {display_name}" if interaction_mode == "Roleplay" else "Conversation with the Bard"
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
                <strong>{display_name}:</strong><br>{message['text']}
            </div>""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center; font-size: 0.85rem; margin-top: 2rem;'>"
    "Crafted with ☕ by <strong>Xixian Huang</strong>"
    "</div>",
    unsafe_allow_html=True
)
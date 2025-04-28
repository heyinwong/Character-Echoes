import streamlit as st
st.set_page_config(page_title="Character Echoes", layout="centered")

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
st.markdown("<h1 class='bard-title'>Character Echoes</h1>", unsafe_allow_html=True)

# Project Mode
st.markdown("<div class='bard-label'>Choose project mode:</div>", unsafe_allow_html=True)
project_mode = st.radio("Choose project mode", ["Shakespeare", "Upload Your Own Story"], label_visibility="collapsed")

uploaded_file = None
uploaded_text = ""
if project_mode == "Upload Your Own Story":
    uploaded_file = st.file_uploader("Upload your story (.txt)", type=["txt"], label_visibility="visible")
    if uploaded_file is not None:
        uploaded_text = uploaded_file.read().decode("utf-8")

if project_mode == "Shakespeare" or (project_mode == "Upload Your Own Story" and uploaded_file is not None):

    if project_mode == "Shakespeare":
        st.markdown("<div class='bard-label'>Choose a Shakespeare play:</div>", unsafe_allow_html=True)
        plays = list_plays()
        default_index = next((i for i, p in enumerate(plays) if "complete works" in p.lower()), 0)
        selected_play = st.selectbox("Select a play", plays, index=default_index, label_visibility="collapsed")
        play_filename = "Complete" if "complete works" in selected_play.lower() else selected_play
        play_text = load_play(play_filename)
    else:
        play_text = uploaded_text

    if project_mode == "Shakespeare":
        st.markdown("<div class='bard-label'>Choose interaction mode:</div>", unsafe_allow_html=True)
        interaction_mode = st.radio("Choose interaction mode", ["Ask the Bard", "Roleplay"], label_visibility="collapsed")
    else:
        interaction_mode = "Roleplay"

    if interaction_mode == "Roleplay":
        if project_mode == "Shakespeare":
            characters = list_characters()
            characters.append("Custom")
            character = st.selectbox("Choose a character", characters, label_visibility="collapsed")
            
            if character == "Custom":
                custom_character = st.text_input("Enter a custom character name:", label_visibility="visible")
                display_name = custom_character.strip() or "Someone You Desired"
            else:
                custom_character = ""
                display_name = character
        else:
            character = None
            custom_character = st.text_input("Enter a character name from your uploaded story:", label_visibility="visible")
            display_name = custom_character.strip() or "Someone You Desired"
        
        current_identity = custom_character if custom_character else character

        if st.session_state.previous_character and current_identity != st.session_state.previous_character:
            st.session_state.chat_history = []
            st.info(f"Chat history cleared — now speaking with {display_name}.")
        st.session_state.previous_character = current_identity

    else:
        character = "The Bard"
        custom_character = ""
        display_name = character

    # Load prompt and suggestion
    if project_mode == "Shakespeare":
        if interaction_mode == "Roleplay":
            instruction, suggestion = load_prompt(character if character != "Custom" else "default")
        else:
            instruction = "You are a wise Shakespearean assistant."
            suggestion = "You can ask for summaries, scene explanations, or famous quotes."
    else:
        instruction = (
            f"You are {custom_character}. Respond only based on the uploaded story. "
            "Do not use external knowledge. Stay in character."
        )
        suggestion = "Ask about events, motivations, or dialogue from the uploaded text."

    # Language style
    st.markdown("<div class='bard-label'>Choose your language style:</div>", unsafe_allow_html=True)
    mode = st.radio("Choose language style", ["Modern English", "Bard Speak"], label_visibility="collapsed")

    # Input section
    input_label = f"Chat with {display_name}" if interaction_mode == "Roleplay" else "Ask the Bard"
    st.markdown(f"<div class='bard-label'>{input_label}</div>", unsafe_allow_html=True)

    st.markdown(
        f"<div class='bard-suggestion'>Try asking {display_name} something like:<br><em>“{suggestion}”</em></div>",
        unsafe_allow_html=True
    )

    user_input = st.text_area("Your message", height=130, label_visibility="collapsed")

    # Buttons
    col1, col2 = st.columns(2)
    with col1:
        respond = st.button("Respond", use_container_width=True)
    with col2:
        clear = st.button("Clear Chat", use_container_width=True)

    if clear:
        st.session_state.chat_history = []
        st.rerun()

    # Generate response
    if respond and user_input.strip():
        persona = instruction + (" Use modern English." if mode == "Modern English" else " Speak in Shakespearean poetic style.")
        messages = [{"role": "system", "content": persona}]

        for m in st.session_state.chat_history:
            messages.append({"role": "user" if m["role"] == "user" else "assistant", "content": m["text"]})

        matches = search_quotes(play_text, user_input)
        if matches:
            quote_context = "\n\n".join(matches)
            messages.append({"role": "system", "content": f"Relevant lines from the story:\n\n{quote_context}"})

        messages.append({"role": "user", "content": user_input})

        with st.spinner("Summoning response..."):
            response = get_openai_response(messages)

        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "bard", "text": response})

    elif respond:
        st.warning("Please enter a message.")

    # Chat history display
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
# utils/styles.py

import streamlit as st
import base64

def set_custom_style():
    with open("assets/background.jpg", "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    background_image = f"data:image/jpeg;base64,{encoded}"

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('{background_image}');
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
        color: #2c2c2c;
    }}

    html, body {{
        font-family: 'Georgia', serif;
        font-size: 18px;
    }}

    section.main {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 16px;
        max-width: 900px;
        margin: 2rem auto;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }}

    h1 {{
        text-align: center;
        font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
        font-size: 2.5rem;
        font-weight: bold;
        color: #fff;
        text-shadow: 1px 1px 1px #fff;
    }}

    /* Reusable label style */
    .bard-label {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 0.4rem 1.2rem;
        border-radius: 12px;
        font-weight: bold;
        color: #a94430;
        font-size: 1.5rem;
        display: inline-block;
        margin-top: 1rem;
        margin-bottom: 0.6rem;
        font-family: 'Georgia', serif;
    }}
    .bard-title {{
        text-align: center;
        font-family: 'Palatino Linotype', 'Book Antiqua', Palatino, serif;
        font-size: 2.8rem;
        font-weight: bold;
        color: white !important;
        text-shadow: 2px 2px 4px #000;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
    }}
    .bard-suggestion {{
        font-size: 0.95rem;
        color: #3a2d1a;
        background-color: #fef7f1;
        padding: 0.75rem 1rem;
        margin-top: 0.25rem;
        margin-bottom: 0.75rem;
        border-left: 4px solid #c76b3e;
        border-radius: 8px;
}}
    /* Inputs */
    textarea, input, .stTextInput, .stTextArea {{
        background-color: #fff !important;
        color: #000 !important;
        border-radius: 8px !important;
        border: 1px solid #999 !important;
    }}

    /* Radio */
    .stRadio > div {{
        background-color: #fff;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
    }}

    /* Buttons */
    .stButton > button {{
        background-color: #333 !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1.2rem !important;
        border-radius: 8px !important;
        font-size: 16px !important;
        font-weight: 500;
        box-shadow: 0 2px 6px rgba(0,0,0,0.3);
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #444 !important;
    }}
    .tight-stack > * {{
    margin-bottom: 0.5rem !important;
}}
    </style>
    """, unsafe_allow_html=True)
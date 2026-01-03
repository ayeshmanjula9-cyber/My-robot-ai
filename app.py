import streamlit as st
import google.generativeai as genai
from streamlit_mic_recorder import speech_to_text
from gtts import gTTS
import os
import base64

st.set_page_config(page_title="My AI Robot", page_icon="🤖")

if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("කරුණාකර Streamlit Secrets වල API Key එක ඇතුළත් කරන්න.")

def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    with open("response.mp3", "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f'<audio autoplay="true"><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>'
        st.markdown(md, unsafe_allow_html=True)

st.title("🤖 මගේ AI යාළුවා")

if os.path.exists("robot.png"):
    st.image("robot.png", width=200)

st.write("පහත මයික්‍රොෆෝනය ඔබා මට කතා කරන්න.")

text_input = speech_to_text(start_prompt="🎤 කතා කරන්න", stop_prompt="🛑 නවත්වන්න", language='en', use_container_width=True, key='recorder')

if text_input:
    st.markdown(f"**ඔබ:** {text_input}")
    with st.spinner("සිතමින් පවතියි..."):
        response = model.generate_content(text_input)
        reply = response.text
        st.markdown(f"**රොබෝ:** {reply}")
        text_to_speech(reply)
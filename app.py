import openai
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
# Set the base URL and API key for the OpenAI client
os.environ["openai.api_base"] = os.getenv("lOCAL_URL" )
os.environ["openai.api_key"] = os.getenv("LOCAL_API_KEY")

st.set_page_config(page_title="Chat with Bot", page_icon="🤖")

st.title("QWEN1.5-7b 🤖")

# Sidebar for API settings
with st.sidebar:
    st.header("Settings")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

# Initialize chat history
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Display chat messages from history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.write(message["content"])

# User input
if prompt := st.chat_input("Type your message"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate assistant response
    try:
        completion = openai.ChatCompletion.create(
            model="model-identifier",
            messages=st.session_state.messages,
            temperature=temperature,
        )
        reply = completion.choices[0].message.content
    except Exception as e:
        reply = "Sorry, I couldn't process your request."

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.write(reply)

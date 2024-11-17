import streamlit as st
import openai
import json

# Configure OpenAI
openai.api_base = "http://localhost:6552/v1"
openai.api_key = "lm-studio"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful."},
        {"role": "assistant", "content": "Hello! I'm your AI assistant powered by LM Studio. I'm here to help answer your questions and engage in meaningful conversations. What would you like to discuss?"}
    ]

st.title("LM Studio Chat Assistant")

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What's on your mind?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            completion = openai.ChatCompletion.create(
                model="LM Studio Community/Meta-Llama-3-8B-Instruct-GGUF",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
                temperature=0.7,
                stream=True,
            )

            # Simulate stream of response with milliseconds delay
            for chunk in completion:
                if 'content' in chunk.choices[0].delta:
                    content = chunk.choices[0].delta.content
                    if content:
                        full_response += content
                        message_placeholder.markdown(full_response + "▌")
            
            message_placeholder.markdown(full_response)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.error("Make sure LM Studio is running and the local server is active on port 6552")
            full_response = "I apologize, but I encountered an error. Please make sure LM Studio is running."
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

# Add a sidebar with some information
with st.sidebar:
    st.title("About")
    st.markdown("""
WARNING:!!!!This is a Streamlit chat interface That runs on my pc!!!!!.
    
**IF NOT WORKING:**
    1. LM Studio not running locally.
    2. Then it's my pc is shut down.
    """)
    
    if st.button("Clear Chat History"):
        st.session_state.messages = [
            {"role": "system", "content": "You are an intelligent assistant made by Dinmay. You always provide well-reasoned answers that are both correct and helpful."},
            {"role": "assistant", "content": "Hello! I'm your AI assistant powered by LM Studio. I'm here to help answer your questions and engage in meaningful conversations. What would you like to discuss?"}
        ]
        st.rerun()

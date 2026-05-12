import streamlit as st
from openai import OpenAI
import os

# Read API Key from Environment Variables
api_key = os.getenv("OPENAI_API_KEY")

# Stop app if API key not found
if not api_key:
    st.error("OPENAI_API_KEY not found.")
    st.stop()

# OpenAI Client
client = OpenAI(api_key=api_key)

# Page Settings
st.set_page_config(
    page_title="ChatGPT Bot",
    page_icon="🤖",
    layout="centered"
)

# App Title
st.title("🤖 Simple ChatGPT Bot")
st.write("Simple chatbot using OpenAI API and Streamlit.")

# Create Chat Memory
if "messages" not in st.session_state:

    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        }
    ]

# Display Previous Messages
for message in st.session_state.messages:

    if message["role"] != "system":

        with st.chat_message(message["role"]):
            st.write(message["content"])

# Chat Input
user_input = st.chat_input("Type your message here...")

# When User Sends Message
if user_input:

    # Display User Message
    with st.chat_message("user"):
        st.write(user_input)

    # Save User Message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    try:

        # Assistant Response
        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                response = client.chat.completions.create(
                    model="gpt-4.1-mini",
                    messages=st.session_state.messages
                )

                bot_reply = response.choices[0].message.content

                st.write(bot_reply)

        # Save Assistant Message
        st.session_state.messages.append({
            "role": "assistant",
            "content": bot_reply
        })

    except Exception as e:

        st.error(f"Error: {e}")
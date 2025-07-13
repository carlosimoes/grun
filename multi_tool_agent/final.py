import os
import sys

# Add the current directory to the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# print(os.getcwd())
import streamlit as st
import uuid
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from .agent import root_agent
from google.genai import types as genai_types

# Set page config
st.set_page_config(page_title="Speaker Agent Chat", page_icon="🔊", layout="centered")
# Constants
USER_ID = f"user-{uuid.uuid4()}"
SESSION_ID = f"session_{uuid.uuid4()}"
APP_NAME = "multi_tool_agent"

if 'root_agent' not in st.session_state:
        st.session_state.root_agent = root_agent
if 'session_service' not in st.session_state:
        st.session_state.session_service = InMemorySessionService()
if 'runner' not in st.session_state:
        st.session_state.runner = Runner(
            agent=st.session_state.code_pipeline_agent, # Use pipeline agent FROM state
            app_name=APP_NAME,
            session_service=st.session_state.session_service
        )
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Echo: {prompt}"
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
import asyncio
import os
import uuid

import streamlit as st
from config import settings
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from multi_tool_agent.streamlit_agent import create_agent_tool

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = settings.vertexai_use
os.environ["GOOGLE_API_KEY"] = settings.google_api


class StreamlitChatbot:
    def __init__(self):
        self.session_service = InMemorySessionService()
        self.runner = None

    async def initialize_session(self):
        """Initialize a new session for the chatbot"""
        if "session_id" not in st.session_state:
            st.session_state.session_id = f"session_{uuid.uuid4()}"
            st.session_state.session = await self.session_service.create_session(
                state={},
                app_name="multi_tool_agent",
                user_id="streamlit_user",
                session_id=st.session_state.session_id,
            )

        if not self.runner:
            self.runner = Runner(
                app_name="multi_tool_agent",
                agent=create_agent_tool(),
                session_service=self.session_service,
            )

    async def get_agent_response(self, user_message: str) -> str:
        """Get response from the agent"""
        content = types.Content(role="user", parts=[types.Part(text=user_message)])

        events = self.runner.run_async(
            session_id=st.session_state.session.id,
            user_id=st.session_state.session.user_id,
            new_message=content,
        )

        async for event in events:
            if event.is_final_response():
                return event.content.parts[0].text

        return "Sorry, I couldn't process your request."


def main():
    st.set_page_config(page_title="AI Assistant Chatbot", page_icon="🤖", layout="wide")

    st.title("🤖 AI Assistant Chatbot")
    st.markdown("Ask me anything! I can help with various tasks and questions.")

    # Initialize chatbot and message history in session_state if they don't exist
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = StreamlitChatbot()
        st.session_state.messages = []
        st.session_state.initialized = False

    # Initialize session asynchronously only if it hasn't been done yet
    if not st.session_state.initialized:
        with st.spinner("Initializing chatbot..."):
            # Use the chatbot instance from session_state to initialize
            asyncio.run(st.session_state.chatbot.initialize_session())
            st.session_state.initialized = True

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get agent response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Use the single, persistent chatbot instance from session_state
                    response = asyncio.run(
                        st.session_state.chatbot.get_agent_response(prompt)
                    )
                    st.markdown(response)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_msg}
                    )

    # Sidebar with additional features (remains the same)
    with st.sidebar:
        st.header("Chat Controls")

        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

        if st.button("New Session"):
            # Clear all session state, including the chatbot object
            st.session_state.clear()
            st.rerun()

        st.header("Session Info")
        if "session_id" in st.session_state:
            st.text(f"Session ID: {st.session_state.session_id[:8]}...")

        st.header("Instructions")
        st.markdown("""
        - Type your questions in the chat input
        - The AI assistant will respond based on your query
        - Use 'Clear Chat History' to start fresh
        - Use 'New Session' to reset everything
        """)


if __name__ == "__main__":
    main()

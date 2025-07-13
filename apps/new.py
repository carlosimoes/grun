import uuid
import streamlit as st
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from multi_tool_agent.agent import root_agent
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
st.subheader("1. Your Request")
user_query = st.text_area("Describe the Python code you want:", height=100, placeholder="e.g., print hello sam in python")

session_service = st.session_state.session_service
runner = st.session_state.runner

# Create a new ADK session for this specific run
session = session_service.create_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# Prepare the initial message
initial_content = genai_types.Content(role='user', parts=[genai_types.Part(text=user_query)])

# Run the pipeline and capture events for detailed logging
with st.spinner("🤖 Running simplified debug sequence..."):
    events = runner.run(
        user_id=USER_ID, session_id=SESSION_ID, new_message=initial_content
    )

    # --- DETAILED EVENT LOGGING ---
    st.write("--- Processing Events ---")
    event_list_for_debug = []
    final_response_text = "Pipeline completed." # Default message
    for i, event in enumerate(events):
        # Safely get attributes, provide default if missing
        event_details = {
            "index": i,
            "id": getattr(event, 'id', 'N/A'),
            "author": getattr(event, 'author', 'N/A'),
            "is_final": event.is_final_response(),
            "interrupted": getattr(event, 'interrupted', None),
            "error_code": getattr(event, 'error_code', None),
            "error_message": getattr(event, 'error_message', None),
            "content_parts": []
        }
        # Check content and parts carefully
        if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts') and event.content.parts:
            for part in event.content.parts:
                part_info = {}
                # Extract text content if present
                if hasattr(part, 'text') and part.text: part_info['text'] = part.text
                # Add other part types if needed and convert complex objects safely
                #todo: remove
                if part_info: # Only add if we extracted something useful
                        event_details["content_parts"].append(part_info)

        event_list_for_debug.append(event_details) # Add structured details for this event

        # Capture final response text from the last agent's message
        if event.is_final_response():
            if hasattr(event, 'content') and event.content and hasattr(event.content, 'parts') and event.content.parts:
                first_part = event.content.parts[0]
                if hasattr(first_part, 'text') and first_part.text:
                    final_response_text = first_part.text # This should be the output of the last (debug) agent

    st.write("DEBUG: Detailed Events List:")
    # Use st.json for potentially large/nested data, start collapsed
    st.json(event_list_for_debug, expanded=False)
    st.write("--- End Processing Events ---")
    # --- END DETAILED EVENT LOGGING ---

# --- Retrieve the final state ---
updated_session = session_service.get_session(
    session_id=SESSION_ID, app_name=APP_NAME, user_id=USER_ID
)
session_state = updated_session.state if updated_session and hasattr(updated_session, 'state') else {}

# Store results in Streamlit's session state for display
st.session_state.results = {
    "final_message": final_response_text # Capture the last agent's direct message
}

if session_state: 
    st.success("Pipeline finished!") 
else: 
    st.warning("Pipeline finished, but session state appears empty.")


# UI Components
st.title("🔊 Speaker Agent Chat")

# Display messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])

# Input for new messages
if st.session_state.session_id:  # Only show input if session exists
    user_input = st.chat_input("Type your message...")
    if user_input:
        send_message(user_input)
        st.rerun()  # Rerun to update the UI with new messages
else:
    st.info("👈 Create a session to start chatting")

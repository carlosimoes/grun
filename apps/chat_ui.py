# agent.py (modify get_tools_async and other parts as needed)
# ./adk_agent_samples/mcp_agent/agent.py
import asyncio
from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from multi_tool_agent.agent import root_agent
import uuid



session_service = InMemorySessionService()
session_id = f"session_{uuid.uuid4()}"    
session = session_service.create_session(
    state={}, app_name='multi_tool_agent', user_id='user_fs', session_id=session_id,
)

# TODO: Change the query to be relevant to YOUR specified folder.
# e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
query = "list files in the tests folder"
print(f"User Query: '{query}'")
content = types.Content(role='user', parts=[types.Part(text=query)])

runner = Runner(
    app_name='multi_tool_agent',
    agent=root_agent,
    session_service=session_service,
)

print("Running agent...")
events = runner.run(
    session_id=session.id, user_id=session.user_id, new_message=content
)

for event in events:
    if event.is_final_response():
        response_text = event.content.parts[0].text
        print(f"Agent Response: '{response_text}'")
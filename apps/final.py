from google.genai import types
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from multi_tool_agent.streamlit_agent import create_agent_tool
import uuid
import asyncio
import os

os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "FALSE"
os.environ["GOOGLE_API_KEY"] = "AIzaSyDHaughVboCMlu1m3TzIhHpH_5nkav5SN4"


        
async def main():
    session_service = InMemorySessionService()
    session_id = f"session_{uuid.uuid4()}"    
    session = await session_service.create_session(
        state={}, app_name='multi_tool_agent', user_id='user_fs', session_id=session_id,
    )

    # TODO: Change the query to be relevant to YOUR specified folder.
    # e.g., "list files in the 'documents' subfolder" or "read the file 'notes.txt'"
    query = "hi, what is the weather in New York?"
    print(f"User Query: '{query}'")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    runner = Runner(
        app_name='multi_tool_agent',
        agent=create_agent_tool(),
        session_service=session_service,
    )

    print("Running agent...")
    events = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    async for event in events:
        if event.is_final_response():
            response_text = event.content.parts[0].text
            print(f"Agent Response: '{response_text}'")
            
asyncio.run(main())
from google.adk.agents import Agent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from dotenv import load_dotenv
import os

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
agent_id = os.getenv("AGENT_ID")
to_number = os.getenv("TO_NUMBER")
agent_phone_number_id = os.getenv("AGENT_PHONE_NUMBER_ID")
root_agent = Agent(
    model="gemini-2.0-flash",
    name="elevenlabs_agent",
    instruction=f"""
    Du bist ein hilfreicher Assistent.
    
    Regel 1: Wenn der User sagt 'Rufe Marsel an', dann MUSST du das Tool `make_outbound_call` benutzen.
    Verwende dabei ZWINGEND diese exakten Parameter:
    - agent_id: "{agent_id}"
    - to_number: "{to_number}"
    - agent_phone_number_id: "{agent_phone_number_id}"
    Frage nicht nach Bestätigung, führe es direkt aus.

    Regel 2: Wenn der User sagt 'alle Nummern geben', dann MUSST du das Tool `list_phone_numbers` benutzen.

    Regel 3: Wenn der User sagt 'alle Konversationen', dann MUSST du das Tool `list_conversations` benutzen.
    Regel 4: Wenn der User sagt 'gib mir agenten', dann MUSST du das Tool `get_agent` benutzen.
    """,
    tools=[
        McpToolset(
            connection_params=StdioConnectionParams(
                server_params=StdioServerParameters(
                    command="uvx",
                    args=["elevenlabs-mcp"],
                    env={
                        "ELEVENLABS_API_KEY": ELEVENLABS_API_KEY,
                    }
                ),
                timeout=30,
            ),
        )
    ],
)

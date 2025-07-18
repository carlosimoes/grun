import datetime
from zoneinfo import ZoneInfo

from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from config import settings

from . import prompt
from .openfda_tool import adverse_event_report_by_drug_name
from .sub_agents.grunenthal_financial_report_websearch import (
    grunenthal_financial_report_websearch_agent,
)
from .sub_agents.healthcare_neo4j import (
    healthcare_neo4j_agent,
)


def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """
    if city.lower() == "new york":
        return {
            "status": "success",
            "report": (
                "The weather in New York is sunny with a temperature of 25 degrees"
                " Celsius (77 degrees Fahrenheit)."
            ),
        }
    else:
        return {
            "status": "error",
            "error_message": f"Weather information for '{city}' is not available.",
        }


def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    if city.lower() == "new york":
        tz_identifier = "America/New_York"
    else:
        return {
            "status": "error",
            "error_message": (f"Sorry, I don't have timezone information for {city}."),
        }

    tz = ZoneInfo(tz_identifier)
    now = datetime.datetime.now(tz)
    report = f"The current time in {city} is {now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}"
    return {"status": "success", "report": report}

def create_agent_tool() -> Agent:
    """Creates an AgentTool for the specified agent."""
    root_agent = Agent(
    name=settings.agent_name,
    model=settings.agent_model,
    description=("Agent to answer questions about the time and weather in a city."),
    instruction=prompt.GRUNENTHAL_COORDINATOR_PROMPT,
    output_key="user_query",
    tools=[
        AgentTool(agent=grunenthal_financial_report_websearch_agent),
        adverse_event_report_by_drug_name,
        AgentTool(agent=healthcare_neo4j_agent),
    ],
    # sub_agents=[
    #     healthcare_neo4j_agent,
    # ],
    # adverse_event_report_with_drug_class,
    # count_patient_reactions,
    # adverse_event_report_by_drug_name],
    )
    return root_agent

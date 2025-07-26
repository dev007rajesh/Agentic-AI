from google.adk import LlmAgent
from google.adk.tools.agent_tool import AgentTool
from . import prompt
from src.utils.firebase_utils import get_data

MODEL = "gemini-2.5-pro"

def get_city_incident_data(city_name):
    """Queries Firebase for incident data for a given city."""
    """
    Retrieves incident data for a specified city from a Firebase database.

    Args:
        city_name (str): The name of the city for which to retrieve incident data.

    Returns:
        dict or None: A dictionary containing the incident data for the specified city,
                      or None if no data is found for the city.
    """
    return get_data(f'city_predictions/{city_name}')

def get_user_frequent_places(sessionId):
    """Queries Firebase for a user's frequent visit places."""
    """
    Retrieves frequent visit places from a user's timeline node in the Firebase database.

    Args:
        sessionId (str): The ID of the user session.

    Returns:
        dict or None: A dictionary containing the incident data for the specified city,
                      or None if no data is found for the city.
    """
    return get_data(f'user_timeline/{sessionId}')

location_agent = LlmAgent(
    name="location_agent",
    model=MODEL,
    description=(
        "This agent provides information about incidents in a particular location, potential difficulties in reaching the location, and necessary precautions."
    ),
    instruction=prompt.LOCATION_AGENT_PROMPT,
    output_key="location_agent_output",
    tools=[
        AgentTool(tool=get_city_incident_data),
        AgentTool(tool=get_user_frequent_places)
    ],
)

root_agent = location_agent

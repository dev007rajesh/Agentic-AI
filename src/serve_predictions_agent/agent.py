from google.adk import Agent
from . import prompt
from utils.firebase_utils import get_data

MODEL = "gemini-2.0-flash"

def get_city_incident_data(city_name: str):
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

def get_user_frequent_places(sessionId: str):
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

root_agent = Agent(
    name="serve_predictions_agent",
    model=MODEL,
    description=(
        "This agent provides information about incidents in a particular location, potential difficulties in reaching the location, and necessary precautions."
    ),
    instruction=prompt.LOCATION_AGENT_PROMPT,
    tools=[
        get_city_incident_data,
        get_user_frequent_places
    ],
)

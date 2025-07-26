from google.adk import Agent
from src.utils.firebase_utils import get_data
from google.adk.models import Gemini

def create_location_agent():
    """Creates a location agent with a suitable instruction."""
    instruction = "You are a helpful assistant that provides information about incidents in a particular location based on user queries. You can also share potential difficulties and precautions a user should follow if they plan to travel to that location, based on the incident data. Use the available tools to fetch relevant information."
    location_agent = Agent(
        name="location_agent",
        model=Gemini(),
        tools=[get_city_incident_data],
        instruction=instruction,
        description="This agent provides information about incidents in a particular location, potential difficulties in reaching the location, and necessary precautions.",
    )
    return location_agent

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

# if __name__ == '__main__':
#     # Example usage (for testing)
#     agent = create_location_agent()
#     print(f"Agent Name: {agent.name}")
#     print(f"Agent Instruction: {agent.instruction}")
#     # To test message handling, you would need to simulate a message object
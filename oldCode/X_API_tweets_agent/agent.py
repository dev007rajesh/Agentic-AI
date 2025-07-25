"""
Agent: GoogleADKAgent
Responsibility: Collect recent posts from X (Twitter) for a specified location.

Instructions:
- Requires an X API token and a tool/library to connect to the X API.
- Replace 'YOUR_X_API_TOKEN' and implement the API call logic as needed.
"""

import requests
from typing import List

import os
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")
print(X_BEARER_TOKEN)

def get_recent_posts(location: str) -> List[dict]:
    """
    Collect recent posts from X (Twitter) for a given location.
    Args:
        location (str): The location or area to search for posts.
    Returns:
        List[dict]: List of recent posts.
    """
    # Search for posts using hashtag of location and read only top 3 posts
    url = "https://api.twitter.com/2/tweets/search/recent"
    headers = {
        "Authorization": f"Bearer {X_BEARER_TOKEN}"
    }
    hashtag = f"#{location.replace(' ', '')}"
    params = {
        "query": hashtag,
        "max_results": 10
    }
    print(f"Request URL: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")
    response = requests.get(url, headers=headers, params=params)
    print(f"Raw Response: {response.text}")
    if response.status_code == 200:
        return response.json().get("data", [])
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return response

from google.adk.agents import Agent

#TODO: update instructions
root_agent = Agent(
    name="X_API_tweets_agent",
    model="gemini-2.0-flash",
    description="Collects recent X (Twitter) posts for a specified location.",
    instruction="""
    You are an autonomous agent responsible for gathering recent posts from X (formerly Twitter) for a user-specified location or area.
    Your workflow:
    1. Accept a location or area as input from the user.
    2. Use the get_recent_posts tool to query the X API.
    3. Ensure you handle API errors gracefully and inform the user if no posts are found or if there is an issue with the token.
    4. Return a concise, readable summary of the most recent posts for the location, including relevant metadata (e.g., timestamp, username, post content).
    5. If requested, support filtering by keywords or time range.
    6. Always respect user privacy and API rate limits.
    """,
    tools=[get_recent_posts],
)

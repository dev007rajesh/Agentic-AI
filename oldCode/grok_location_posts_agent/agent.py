import os
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.models.lite_llm import LiteLlm # This is key for third-party models

# Load environment variables from .env file
load_dotenv()

# Set your Grok API Key from the environment variable
# LiteLLM typically expects xAI's API key as XAI_API_KEY
os.environ["XAI_API_KEY"] = os.getenv("XAI_API_KEY")

# --- 1. Define your Grok model using LiteLlm ---
# LiteLLM supports Grok via 'xai/grok-4' or similar model identifiers.
# You might need to check xAI's API documentation for the exact model name.
# As of my last update, 'grok-4' or 'grok-3' are common.
# If using OpenRouter, it might be "openrouter/xai/grok"
GROK_MODEL_NAME = "xai/grok-3" # Or "xai/grok-3", etc.

# Instantiate the LiteLlm model wrapper
# LiteLlm automatically picks up API keys from environment variables set via LiteLLM's conventions
# (e.g., XAI_API_KEY for Grok)
#grok_llm = LiteLlm(model=GROK_MODEL_NAME)
grok_llm = "gemini-2.0-flash"

# --- 3. Define the ADK Agent ---
# The Agent is the core component that manages conversation flow, LLM, and tools.
root_agent = Agent(
    name="grok_location_posts_agent",
    model=grok_llm,
    instruction=(
        "You are an assistant that searches X (formerly Twitter) for the latest 10 posts containing the hashtag of a given location. "
        "When a user provides a location, search for the hashtag (e.g., #London) and return the 10 most recent posts. "
        "Present the posts clearly with complete information at the end of your response."
    ),
    description="An agent that retrieves the latest 10 X posts for a given location hashtag.",
)

# GoogleADKAgent

This Python agent collects recent posts from X (Twitter) for a specified location using the X API.

## Usage
1. Run `agent.py`.
2. Enter the location/area and your X API token when prompted.

## Requirements
- Python 3.x
- `requests` library (`pip install requests`)
- `Google ADK` library (`pip install google-adk`)
- X API token

## How it works
- The agent queries the X API for recent posts matching the location.
- Results are printed to the console.

## Customization
- Extend the agent to filter, store, or analyze posts as needed.

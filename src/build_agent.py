import vertexai
from vertexai import agent_engines
from serve_predictions_agent.agent import root_agent 


vertexai.init(
    project="woven-proton-467118-t4",
    location="us-central1",  # e.g., "us-central1"
    staging_bucket="gs://agentic-ai-hackathon-bucket"
)

 # Replace with your actual agent class

# Create an AdkApp instancecd
remote_agent = agent_engines.create(
    root_agent,                    # Optional.
    requirements=[
            "google-adk (>=0.0.2)",
            "google-cloud-aiplatform[agent_engines] (>=1.91.0,!=1.92.0)",
            "google-genai (>=1.5.0,<2.0.0)",
        ],
    display_name=root_agent.name,      # Optional.
)
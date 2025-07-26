from google.adk import Agent

# Import necessary components for your agent
# from google.adk.tools import CodeInterpreterTool
# from google.adk.models import Gemini

def create_root_agent(instruction):
    # --- Define the ADK Agent ---
    # The Agent is the core component that manages conversation flow, LLM, and tools.
    root_agent = Agent(
        name="root_agent",
        # model=Gemini(model="gemini-1.5-flash-latest"),  # Replace with your chosen model
        # tools=[CodeInterpreterTool()],  # Add any tools your agent needs
        instruction=instruction,
        description="This is the root agent.",
    )
    return root_agent

# if __name__ == '__main__':
#     # Example usage (for testing)
#     instruction = "Hello, I am the root agent."
#     agent = create_root_agent(instruction)
#     print(f"Agent Name: {agent.name}")
#     print(f"Agent Instruction: {agent.instruction}")
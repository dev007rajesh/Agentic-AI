from flask import Flask, request, jsonify
from oldCode.grok_location_posts_agent.agent import create_grok_location_posts_agent

app = Flask(__name__)

@app.route('/process_location', methods=['GET'])
def process_location():
    location = request.args.get('location')

    if not location:
        return jsonify({"error": "Invalid request, please provide a location parameter in the URL."}), 400

    # Define the instruction based on the provided location
    instruction = f"Find events/incidents/activies that are happening in {location} location in banglore and share me in the json format of the posts with title, likes,diskes, reactions, few comments"

    # Create and invoke the agent with the specific instruction
    location_agent = create_grok_location_posts_agent(instruction)
    
    # Process the turn with a message to trigger the agent's logic
    # The exact message might depend on how the agent is designed to be triggered
    # For this agent, simply providing the location again in the message might work, 
    # or a generic trigger phrase like "Process location" might be needed.
    # Let's assume a generic trigger phrase for now.
    response = location_agent.process_turn(f"Process location: {location}")

    # Return the agent's response
    return jsonify({"status": "success", "response": response.text})

if __name__ == '__main__':
    app.run(debug=True)

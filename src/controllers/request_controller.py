from flask import Flask, request, jsonify
from src.utils.firebase_utils import get_data, post_data
import uuid
from src.agents.location_agent import create_location_agent

app = Flask(__name__)

@app.route('/get_predictions', methods=['GET'])
def get_predictions_route():
    city = request.args.get('city')
    location = request.args.get('location')
    sessionId = request.args.get('sessionId')

    if sessionId and location:
        user_timeline = get_data(f'user_timeline/{sessionId}')
        if user_timeline is None:
            user_timeline = {'locations': []}
        user_timeline['locations'].append(location)
        user_timeline['locations'] = user_timeline['locations'][-50:]
        post_data(f'user_timeline/{sessionId}', user_timeline)
    city = request.args.get('city')
    if not city:
        return jsonify({"status": "error", "message": "city is a required query parameter.", "error_code": 400}), 400

    predictions = get_data(f'city_predictions/{city}')

    if predictions is not None:
        return jsonify({"status": "success", "data": predictions})
    else:
        return jsonify({"status": "error", "message": f"Could not retrieve predictions for {city}.", "error_code": 500}), 500

@app.route('/process_user_content', methods=['POST'])
def process_user_content():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON).", "error_code": 400}), 400
    
    if not any(key in data for key in ['text', 'image', 'location']):
        return jsonify({"status": "error", "message": "At least one of text, image, or location must be provided.", "error_code": 400}), 400
    
    data['id'] = str(uuid.uuid4()) # Add a unique ID
    # Save the data to Firebase under 'user_posts'

    success = post_data('user_posts', data)
    if success:
        return jsonify({"status": "success", "message": "User content received and saved."})
    else:
        return jsonify({"status": "error", "message": "Failed to save user content.", "error_code": 500}), 500

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.json
    if not data or 'prompt' not in data:
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON or prompt).", "error_code": 400}), 400

    prompt = data['prompt']

    # Create the location agent
    location_agent = create_location_agent()

    try:
        # Send the message to the agent and get the response
        agent_response = location_agent.process_turn(prompt)

        # Assuming the agent_response has a 'response' attribute containing the generated text
        generated_response = agent_response.response

    except Exception as e:
        # Handle any errors during agent interaction
        return jsonify({"status": "error", "message": f"Error generating response from agent: {str(e)}", "error_code": 500}), 500

    return jsonify({"status": "success", "response": generated_response})


if __name__ == '__main__':
    app.run(debug=True)
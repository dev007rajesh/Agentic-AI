from flask import Flask, request, jsonify
from src.utils.firebase_utils import get_data, post_data
import uuid
from src.agents.location_agent import create_location_agent
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

@app.route('/get_predictions', methods=['GET'])
def get_predictions_route():
    logging.info("Received request for /get_predictions")
    city = request.args.get('city')
    location = request.args.get('location')
    sessionId = request.args.get('sessionId')
    logging.info(f"Parameters: city={city}, location={location}, sessionId={sessionId}")

    if sessionId and location:
        user_timeline = get_data(f'user_timeline/{sessionId}')
        if user_timeline is None:
            user_timeline = {'locations': []}
        user_timeline['locations'].append(location)
        user_timeline['locations'] = user_timeline['locations'][-50:]
        post_data(f'user_timeline/{sessionId}', user_timeline)
    city = request.args.get('city')
    if not city:
        logging.error("Missing city parameter in /get_predictions request")
        return jsonify({"status": "error", "message": "city is a required query parameter.", "error_code": 400}), 400

    predictions = get_data(f'city_predictions/{city}')

    if predictions is not None:
        logging.info(f"Successfully retrieved predictions for {city}")
        return jsonify({"status": "success", "data": predictions})
    else:
        logging.warning(f"Could not retrieve predictions for {city}")
        return jsonify({"status": "error", "message": f"Could not retrieve predictions for {city}.", "error_code": 500}), 500

@app.route('/process_user_content', methods=['POST'])
def process_user_content():
    logging.info("Received request for /process_user_content")
    data = request.json
    logging.info(f"Request payload: {data}")
    if not data:
        logging.error("Invalid request payload (missing JSON) in /process_user_content")
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON).", "error_code": 400}), 400
    
    if not any(key in data for key in ['text', 'image', 'location']):
        logging.error("Missing text, image, or location in /process_user_content payload")
        return jsonify({"status": "error", "message": "At least one of text, image, or location must be provided.", "error_code": 400}), 400
    
    data['id'] = str(uuid.uuid4()) # Add a unique ID
    # Save the data to Firebase under 'user_posts'
    logging.info(f"Saving user content with ID: {data['id']}")
    success = post_data('user_posts', data)
    if success:
        logging.info("Successfully saved user content")
        return jsonify({"status": "success", "message": "User content received and saved."})
    else:
        logging.error("Failed to save user content")
        return jsonify({"status": "error", "message": "Failed to save user content.", "error_code": 500}), 500

@app.route('/generate_response', methods=['POST'])
def generate_response():
    logging.info("Received request for /generate_response")
    data = request.json
    logging.info(f"Request payload: {data}")
    if not data or 'prompt' not in data:
        logging.error("Invalid request payload (missing JSON or prompt) in /generate_response")
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON or prompt).", "error_code": 400}), 400

    prompt = data['prompt']
    logging.info(f"Prompt received: {prompt}")

    # Create the location agent
    location_agent = create_location_agent()
    logging.info("Location agent created")

    try:
        # Send the message to the agent and get the response
        agent_response = location_agent.process_turn(prompt)
        logging.info("Received response from location agent")

        # Assuming the agent_response has a 'response' attribute containing the generated text
        generated_response = agent_response.response
        logging.info(f"Generated response: {generated_response}")

    except Exception as e:
        logging.error(f"Error generating response from agent: {str(e)}", exc_info=True)
        # Handle any errors during agent interaction
        return jsonify({"status": "error", "message": f"Error generating response from agent: {str(e)}", "error_code": 500}), 500

    return jsonify({"status": "success", "response": generated_response})


if __name__ == '__main__':
    app.run(debug=True)
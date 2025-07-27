from flask import Flask, request, jsonify
from utils.firebase_utils import get_data, post_data
import uuid
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

if __name__ == '__main__':
    app.run(debug=True)
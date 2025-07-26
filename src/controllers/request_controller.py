from flask import Flask, request, jsonify
from src.agents.root_agent import RootAgent  # Assuming this is the correct import path

app = Flask(__name__)

# Initialize the Root Agent
root_agent = RootAgent()

@app.route('/process_request', methods=['POST'])
def process_request():
    data = request.json

    if not data:
        return jsonify({"status":from flask import Flask, request, jsonify
from src.agents.location_processing_agent import LocationProcessingAgent
from src.agents.incident_reporting_agent import IncidentReportingAgent

app = Flask(__name__)

# Initialize the specific agents
location_processing_agent = LocationProcessingAgent()
incident_reporting_agent = IncidentReportingAgent()

@app.route('/process_location_data', methods=['POST'])
def process_location_data():
    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON).", "error_code": 400}), 400

    # Basic validation for Request Type 1 data
    # You should add more comprehensive validation here based on your data requirements
    if "area" not in data:
         return jsonify({"status": "error", "message": "Missing 'area' in request payload.", "error_code": 400}), 400


    # Pass the validated data directly to the Location Processing Agent
    response = location_processing_agent.process(data)

    return jsonify(response), 200


@app.route('/process_incident_report', methods=['POST'])
def process_incident_report():
    data = request.json

    if not data:
        return jsonify({"status": "error", "message": "Invalid request payload (missing JSON).", "error_code": 400}), 400

    # Basic validation for Request Type 2 data
    # You should add more comprehensive validation here based on your data requirements
    if "incident_details" not in data:
         return jsonify({"status": "error", "message": "Missing 'incident_details' in request payload.", "error_code": 400}), 400

    # Pass the validated data directly to the Incident Reporting Agent
    response = incident_reporting_agent.process(data)

    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
 "error", "message": "Invalid request payload (missing JSON).", "error_code": 400}), 400

    request_type = data.get("request_type")

    if request_type is None:
        return jsonify({"status": "error", "message": "Invalid user request (missing 'request_type').", "error_code": 400}), 400

    if request_type not in [1, 2]:
        return jsonify({"status": "error", "message": "Invalid user request (invalid 'request_type').", "error_code": 400}), 400

    # If the request is valid, pass it to the Root Agent
    response = root_agent.process(data)

    return jsonify(response), 200 # Assuming the agent returns a status code within the response or we'll set it here


if __name__ == '__main__':
    # This is for local testing. For production deployment (e.g., on Vertex AI),
    # you would typically use a production-ready web server like Gunicorn.
    app.run(debug=True, port=5000)

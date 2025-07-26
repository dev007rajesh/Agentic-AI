import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase Admin SDK (replace with your actual credentials file and database URL)
cert_path = 'src/utils/agentic-ai-hackathon-478c0-firebase-adminsdk-fbsvc-2436bafee9.json' # <---- IMPORTANT: Replace with your file path
database_url = 'https://agentic-ai-hackathon-478c0-default-rtdb.firebaseio.com/' # <---- IMPORTANT: Replace with your database URL

try:
    cred = credentials.Certificate(cert_path)
    firebase_admin.initialize_app(cred, {
        'databaseURL': database_url
    })
except Exception as e:
    print(f"Error initializing Firebase: {e}")
    print(f"Please make sure the Firebase credentials file exists at {cert_path}")
    print("and the database URL is correctly set.")


def get_data(path):
    """Retrieves data from a specified path in the Firebase Realtime Database."""
    try:
        ref = db.reference(path)
        data = ref.get()
        return data
    except Exception as e:
        print(f"Error getting data from Firebase at path '{path}': {e}")
        return None


def post_data(path, data):
    """Posts data to a specified path in the Firebase Realtime Database."""
    try:
        ref = db.reference(path)
        ref.set(data)
        return {"status": "success", "message": f"Data successfully posted to path '{path}'."}
    except Exception as e:
        print(f"Error posting data to Firebase at path '{path}': {e}")
        return {"status": "error", "message": f"Error posting data to Firebase at path '{path}': {e}"}

# Example Usage (for testing)
#if __name__ == '__main__':
    # Example of getting data
    # Replace 'your/data/path' with an actual path in your database
    # retrieved_data = get_data('your/data/path')
    # print(f"Retrieved Data: {retrieved_data}")

    # Example of posting data
    # Replace 'your/new/data/path' and the data dictionary with your desired values
    # data_to_post = {'key1': 'value1', 'key2': 'value2'}
    # post_result = post_data('your/new/data/path', data_to_post)
    # print(f"Post Result: {post_result}")
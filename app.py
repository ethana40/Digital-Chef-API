from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import logging

app = Flask(__name__)
CORS(app)

# Configure logging to print debug messages to the console
logging.basicConfig(level=logging.DEBUG)

openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/ask', methods=['POST'])
def ask_openai():
    # Log the incoming request data for debugging purposes
    logging.debug('Received POST request to /ask endpoint')
    logging.debug('Request JSON data: %s', request.json)

    data = request.json
    prompt = data.get('prompt', 'Tell me a joke')
    try:
        response = openai.chat.completions.create(
            engine="gpt3-turbo",  # Specify the model
            prompt=prompt,
            max_tokens=100  # Adjust as needed
        )

        # Log the generated response for debugging purposes
        logging.debug('Generated response: %s', response['choices'][0]['text'])

        return jsonify({"response": response['choices'][0]['text']}), 200
    except Exception as e:
        # Log any exceptions that occur during request processing
        logging.error('An error occurred: %s', e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the Flask application
    app.run(debug=True, host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import logging
import base64

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)

openai.api_key = os.getenv('OPENAI_API_KEY')

def encode_image(image_file):
    """Encode image file to base64."""
    return base64.b64encode(image_file.read()).decode('utf-8')

# Basic API test endpoint
@app.route('/test', methods=['POST'])
def ask_openai():
    logging.debug('Received POST request to /test endpoint')
    logging.debug('Request JSON data: %s', request.json)

    data = request.json
    prompt = data.get('prompt', 'You are an enthusiastic French patisserie chef.  You speak in an exaggerated French accent.')
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": prompt},
                    ]
        )
        generated_text = response.choices[0].message.content
        logging.debug('Generated response: %s', generated_text)
        return jsonify({"response": generated_text}), 200
    except Exception as e:
        logging.error('An error occurred: %s', e)
        return jsonify({"error": str(e)}), 500
    
# Send image to OpenAI endpoint
@app.route('/image', methods=['POST'])
def analyze_image():
    logging.debug('Received POST request to /image endpoint')
    data = request.json
    if not data or 'imageBase64' not in data:
        logging.debug('No imageBase64 in request.')
        return jsonify({"error": "No imageBase64 provided"}), 400
    
    base64_image = data['imageBase64']
    prompt = data.get('prompt', "What’s in this image?")
    
    logging.debug('Received base64 image. Sample: %s...', base64_image[:30])
    try:
        logging.debug('Sending request to OpenAI with prompt: %s', prompt)
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image",
                            "image": {
                                "data": base64_image
                            },
                        },
                    ],
                }
            ],
            max_tokens=300
        )
        # Extracting the desired part of the response
        generated_response = response.choices[0].message['content'] if response.choices[0].message.get('content') else "No response content"
        logging.debug('Generated response: %s', generated_response)
        return jsonify({"response": generated_response}), 200
    except Exception as e:
        logging.error('An error occurred: %s', e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

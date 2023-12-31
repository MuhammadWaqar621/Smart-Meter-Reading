from flask import Flask, request, jsonify
import os
import concurrent.futures
import asyncio
import datetime
from main import pipeline

import base64

app = Flask(__name__)

# Define a directory to store uploaded images
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

# Define a list of valid API keys (replace with your actual API keys)
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

def process_image(image_data):
    try:
        # Decode base64 image data
        image_content = base64.b64decode(image_data)
        image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Save the decoded image in the uploads folder
        image_path = os.path.join(upload_dir, f"{image_name}.jpeg")
        with open(image_path, "wb") as temp_image_file:
            temp_image_file.write(image_content)

        try:
            status, message, result, path = pipeline(source=image_path)
            # print(path)
            from pathlib import Path
            if Path(path).exists():
                img64 = image_to_base64(path)
            else:
                img64 = path
        except Exception as e:
            return {"error": f"OCR error: {str(e)}"}

        try:
            os.remove(image_path)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        response = {
            "status": status,
            "message": message,
            "data": {
                "outputImage": img64,
                "meterNumber": result
            }
        }
        return response
    except Exception as e:
        return {"error": str(e)}

# Validate the API key
def get_api_key():
    api_key = request.headers.get("api_key")
    if api_key not in user_api_keys.values():
        return jsonify({"error": "Invalid API key"}), 401
    return api_key

@app.route("/Smart_Meter/", methods=["POST"])
def smart_meter_endpoint():
    try:
        api_key = get_api_key()
        image_data = request.files["image_data"].read()
        result = process_image(image_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1003, debug=True)

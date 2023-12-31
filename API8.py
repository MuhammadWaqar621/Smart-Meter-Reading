from fastapi import FastAPI, Depends, HTTPException, Header, File
import os
import concurrent.futures
import asyncio
import datetime
from main8 import pipeline

import base64
def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_encoded = base64.b64encode(image_file.read()).decode("utf-8")
    return base64_encoded

app = FastAPI()

# Define a directory to store uploaded images
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

# Define a list of valid API keys (replace with your actual API keys)
user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}


def process_image(image_data: bytes):
    try:
        # Decode base64 image data
        image_content = base64.b64decode(image_data)
        image_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")

        # Save the decoded image in the uploads folder
        image_path = os.path.join(upload_dir, f"{image_name}.jpeg")
        with open(image_path, "wb") as temp_image_file:
            temp_image_file.write(image_content)

        try:
            status,message, result,path = pipeline(source=image_path)
            # print(path)
            from pathlib import Path
            if Path(path).exists():
                img64=image_to_base64(path)
            else:
                img64=path
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


# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key


@app.post("/Smart_Meter/")
async def Smart_Meter_endpoint(
    image_data: str = File(...),
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's image
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_image(image_data)
        )
    return result


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1004, reload=True)
# uvicorn API8:app --host 0.0.0.0 --port 1004 --reload
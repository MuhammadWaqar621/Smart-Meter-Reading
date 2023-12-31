from fastapi import FastAPI, UploadFile, Depends, HTTPException, Header
from fastapi.security.api_key import APIKeyHeader
import os
import concurrent.futures
import asyncio
import zipfile
import shutil
from fastapi.responses import FileResponse
import datetime
from main8 import pipeline            
import json 

app = FastAPI()


# Define a directory to store uploaded videos
upload_dir = "uploads"
os.makedirs(upload_dir, exist_ok=True)

# Define a list of valid API keys (replace with your actual API keys)

user_api_keys = {
    "user1": "apikey1",
    "user2": "apikey2",
    # Add more users and their API keys as needed
}
def process_image(video_file: UploadFile):
    try:
        # Read the uploaded video file into memory
        video_content = video_file.file.read()
        video_name = os.path.splitext(video_file.filename)[0]
        # Save the uploaded video in the video folder
        video_file_path = os.path.join(upload_dir, f"{video_name}.jpeg")
        with open(video_file_path, "wb") as temp_video_file:
            temp_video_file.write(video_content)
        try:
            status,result=pipeline(source=video_file_path)
            
            # print('image paath ',image_path)
        except Exception as e:
            return {"error": f"OCR error: {str(e)}"}

        try:
            os.remove(video_file_path)
        except Exception as e:
            return {"error": f"File delete error: {str(e)}"}

        
        # return {"results": "done"}
        # Send the zip file as a response
        # response=FileResponse(f"{video_name}.zip", filename=f'{video_name}.zip')
        # os.remove(f"{video_name}.zip")
        # return response
        # return "image"
        # return result
        return {"status":status,
                           "meterNumber": result}
    except Exception as e:
        return {"error": str(e)}

# Dependency to validate the API key
async def get_api_key(api_key: str = Header(None, convert_underscores=False)):
    if api_key not in user_api_keys.values():
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.post("/Smart_Meter/")
async def Smart_Meter_endpoint(
    image_file: UploadFile,
    api_key: str = Depends(get_api_key),  # Require API key for this route
):
    # Create a new thread for processing each user's video
    with concurrent.futures.ThreadPoolExecutor() as executor:
        result = await asyncio.get_event_loop().run_in_executor(
            executor,
            lambda: process_image(image_file)
        )
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=1004, reload=True)
# uvicorn app8:app --host 0.0.0.0 --port 1004 --reload
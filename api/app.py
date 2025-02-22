from fastapi import FastAPI, Query
import subprocess
import json

app = FastAPI()

@app.get("/generate")
async def generate(
    prompt: str, 
    image_url: str, 
    format: str = "landscape", 
    numberofimages: int = 1
):
    # Ensure number of images doesn't exceed the limit
    if numberofimages > 5:
        numberofimages = 5

    # Run the Python script
    command = f'python flux1.py --prompt "{prompt}" --image_url "{image_url}" --format {format} --numberofimages {numberofimages}'
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Extract URLs from the output
    urls = [line.split(": ")[1].strip() for line in result.stdout.split("\n") if "Generated Image" in line]
    
    return {"urls": urls}

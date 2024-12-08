#!/home/nakul/Desktop/clado-sample-project/venv/bin/python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

# Create FastAPI instance
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define data model
class FormData(BaseModel):
    name: str
    description: str

@app.post("/")
async def receive_data(data: FormData):
    print(f"Received name: {data.name}")
    print(f"Received description: {data.description}")
    return {"status": "success", "message": "Data received successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

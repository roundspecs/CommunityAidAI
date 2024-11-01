import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile

from app.services import CaptionService, SolutionService

app = FastAPI(
    title="CommunityAidAI",
    description="An API service that analyzes images and text descriptions to propose solutions for community issues.",
    version="1.0.0",
)

caption_service = CaptionService()
solution_service = SolutionService()

@app.post("/caption")
async def get_caption(file: UploadFile = File(...)):
    # save the file temporarily
    with open("temp.jpg", "wb") as buffer:
        buffer.write(file.file.read())
    # generate caption
    caption = caption_service.generate_caption("temp.jpg")
    # remove the temporary file
    os.remove("temp.jpg")

    return {"caption": caption}

@app.get("/solution")
async def get_solution(caption: Optional[str], description: str):
    return {"solutions": solution_service.generate_solution(caption, description)}

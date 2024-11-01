import os
from typing import Optional

from fastapi import FastAPI, File, UploadFile

from app.services import CaptionService, SolutionService, StepsService

app = FastAPI(
    title="CommunityAidAI",
    description="An API service that analyzes images and text descriptions to propose solutions for community issues.",
    version="1.0.0",
)

caption_service = CaptionService()
solution_service = SolutionService()
steps_service = StepsService()


@app.post("/caption")
async def get_caption(file: UploadFile = File(...)):
    with open("temp.jpg", "wb") as buffer:
        buffer.write(file.file.read())
    caption = caption_service.generate_caption("temp.jpg")
    os.remove("temp.jpg")

    return {"caption": caption}


@app.get("/solutions")
async def get_solution(caption: Optional[str], description: str):
    return {
        "solutions": solution_service.generate_solution(caption, description),
    }


@app.get("/steps")
async def get_steps(caption: str, description: str, solution: str):
    return {
        "steps": steps_service.generate_solution(
            caption,
            description,
            solution,
        ),
    }

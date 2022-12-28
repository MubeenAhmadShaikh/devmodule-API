from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from devmodule.core.database import Base, engine
from devmodule.core import models
from devmodule.router import project, skill, authentication, profile, review
from pathlib import Path
import uvicorn
app = FastAPI()

models.Base.metadata.create_all(engine)
origins = [
    "http://127.0.0.1:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(authentication.router)
app.include_router(profile.router)
app.include_router(skill.router)
app.include_router(project.router)
app.include_router(review.router)



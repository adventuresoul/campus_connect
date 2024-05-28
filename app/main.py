from fastapi import FastAPI
from app import models
from app.database import engine
from app.routers import posts, users, auth, vote
from fastapi.middleware.cors import CORSMiddleware


# Create all tables, here we migrate
#models.Base.metadata.create_all(bind = engine)

# FastAPI instance
app = FastAPI()

origins = ["*"] # all IPs

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Routes
@app.get("/")
def root():
    return {"message": "Hello World, welcome to campus connect"}






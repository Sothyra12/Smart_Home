from fastapi import FastAPI
from app.api.endpoints import user
from app.db.session import engine
from app.models import user as user_model
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import auth

user_model.Base.metadata.create_all(bind=engine)

app = FastAPI(title="SynHome API")


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(user.router, prefix="/api/v1/users", tags=["users"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SynHome API"}
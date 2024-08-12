from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import user, auth, rooms_router, devices_router
from app.db.session import engine
from app.models import user as user_model
from app.models.login import LoginRequest

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
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(rooms_router, prefix="/api/v1/rooms", tags=["rooms"])
app.include_router(devices_router, prefix="/api/v1/devices", tags=["devices"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SynHome API"}

# New endpoints
@app.post("/login")
async def login(request: LoginRequest):
    if request.username == "admin" and request.password == "secret":
        return {"message": "Login successful"}
    raise HTTPException(status_code=401, detail="Invalid credentials")
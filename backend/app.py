from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
import uvicorn
import dotenv
import os
import json

env = os.getenv("ENV", "development")
dotenv.load_dotenv(f".env.{env}", override=True)

from routers import user, admin
from database import postgresql_db
from model import UserLogin

app = FastAPI()

app.add_event_handler("startup", postgresql_db.connect)
app.add_event_handler("shutdown", postgresql_db.disconnect)

@app.post("/login")
async def login(request: UserLogin):
    """
    Login endpoint to verify user credentials.
    """
    username = request.username
    password = request.password

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    try:
        user = await postgresql_db.login(username=username, password=password)
        return JSONResponse(content={
            "message": "Login successful",
            "user_id": user['id'],
            "metadata": json.loads(user['metadata'])
        }, status_code=200)
    except ValueError:
        raise HTTPException(status_code=401, detail="Wrong username or password")

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/ping")
async def ping_check():
    """
    Ping check endpoint to verify the HTTP request can be reached from the frontend.
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

async def router_admin_filter(request: Request):
    """
    Filter to check if the request header contains a valid admin user.
    """
    user_id = request.headers.get("user_id")
    user_profile = await postgresql_db.get_user(user_id)


    if json.loads(user_profile["metadata"])["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="User not allowed to access this resource"
        )

async def router_header_filter(request: Request):
    """
    Filter to check if the request header contains a valid user.
    """
    user_id = request.headers.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=403,
            detail="Not found user, please login first"
        )    
    
    user_profile = await postgresql_db.get_user(user_id)

    if not user_profile:
        raise HTTPException(
            status_code=403,
            detail="Invalid user, please login first"
        )

app.include_router(user.router, prefix="/chatbot", tags=["chatbot"], dependencies=[Depends(router_header_filter)])
app.include_router(admin.router, prefix="/admin", tags=["admin"], dependencies=[Depends(router_header_filter), Depends(router_admin_filter)])

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)

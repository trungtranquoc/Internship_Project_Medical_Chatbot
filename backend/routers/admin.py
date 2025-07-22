from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from database import postgresql_db
from model import NewUser

router = APIRouter()

@router.get("/show_all_users")
async def show_all_users():
    """
    Endpoint to retrieve all users in the system.
    """
    users = await postgresql_db._all_users()
    
    if not users:
        return JSONResponse(content={"message": "No users found"}, status_code=404)
    
    # Users are already serialized in the database layer
    # But we use jsonable_encoder as an extra safety measure
    return JSONResponse(content=jsonable_encoder(users), status_code=200)

@router.post("/create_account")
async def create_account(request: NewUser):
    """
    Endpoint to create a new user account.
    """
    username = request.username
    password = request.password
    name = request.name
    role = request.role or "user"

    if not username or not password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    result = await postgresql_db.create_user(username=username, password=password, name=name, role=role)

    return JSONResponse(content={"message": "User created successfully", "user_id": str(result["user_id"])}, status_code=201)
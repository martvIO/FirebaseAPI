from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from typing import Optional
import jwt, os, firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime, timedelta

# Router setup
router = APIRouter(
    prefix="/auth",
    tags=['auth']
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get the current working directory
current_directory = Path(__file__).resolve().parent

# Construct the path to the .env file two folders back
env_path = current_directory.parent.parent / '.env'

# Load the environment variables from the .env file
load_dotenv(dotenv_path=env_path)

# Now you can access the secret key from the environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 129600
# OAuth2PasswordBearer creates a dependency that will require the user to send the token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Firebase initialization
cred = credentials.Certificate("C:/Users/Maroun issa/FirebaseAPI/app/database-b81ee-firebase-adminsdk-6w3fp-bffce38e46.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://database-b81ee-default-rtdb.firebaseio.com/'
})

# Reference to the users section in Firebase Realtime Database
dp = db.reference('users')

# Models for input data
class SignupData(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Helper functions for password hashing and token creation
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user(username: str):
    user_snapshot = dp.child(username).get()
    return user_snapshot
import json

  # Convert JSON string to dictionary

def get_users():
    return dp.order_by_child("email")

@router.post("/signup")
def signup(signup_data: SignupData):
    existing_user = get_user(signup_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    for user in dp.get():
        if user == signup_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(signup_data.password)
    user_data = {
        "username": signup_data.username,
        "first_name": signup_data.first_name,
        "last_name": signup_data.last_name,
        "email": signup_data.email,
        "hashed_password": hashed_password
    }
    dp.child(signup_data.username).set(user_data)
    
    return {"message": "User created successfully"}

# POST /auth/login using OAuth2PasswordRequestForm
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user(form_data.username)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# Dependency to get the current user from token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except jwt.PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

# Example protected route (requires token)
@router.get("/users/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "first_name": current_user["first_name"],
        "last_name": current_user["last_name"],
        "email": current_user["email"]
    }

# DELETE /auth/delete_account
@router.delete("/delete_account")
def delete_account(current_user: dict = Depends(get_current_user)):
    username = current_user["username"]
    
    # Check if the user exists
    user = get_user(username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Remove user data from the Realtime Database
    dp.child(username).delete()

    return {"message": f"User '{username}' deleted successfully"}
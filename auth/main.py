from fastapi import Depends, FastAPI,Depends, HTTPException, status 
from sqlalchemy.orm import Session
from auth import models
import model, schemas,utils
from auth_database import get_db
from jose import  jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordRequestForm


SECRET_KEY = "" 
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



# Helper fuctions that takes user data

def create_access_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

app = FastAPI()

@app.post("/signup")
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
     
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code= 400, detail="Username already exist")
    

    
    hashed_password = utils.hash_password(user.password)
    new_user = models.User(email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username, "email": new_user.email, "role": new_user.role}
 

@app.post("/login")  
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username")
    
    if not utils.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")
    
    token_data  = {'sub': user.username, 'role': user.role }
    token = create_access_token(data=token_data)
    return {"access_token": token, "token_type": "bearer"}
    

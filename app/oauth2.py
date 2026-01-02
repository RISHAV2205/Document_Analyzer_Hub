from jose import JWTError,jwt
from datetime import timezone,datetime,timedelta
from . import schema
from fastapi import Depends,status,HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
load_dotenv() 

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="login")  #auth login url
#SECRET KEY
#ALGORITHM
#EXPIRATION TIME


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# print("SECRET_KEY:", SECRET_KEY, type(SECRET_KEY))

def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    print(to_encode)
    
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    
    return encoded_jwt
    
    
def verify_access_token(token:str,credential_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id: str=payload.get("user_id")
    
        if id is None:
            raise credential_exception
        token_data=schema.TokenData(id=user_id)
    except JWTError:
        raise credential_exception
    return token_data
        
def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail=f"couldnot validate credentials",headers={"WWW-Authenticate":"Bearer"})
    return verify_access_token(token,credentials_exception)
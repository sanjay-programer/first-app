from fastapi import APIRouter,status,HTTPException
from app.schemas import New_User
from app.utils import hash
from app.DataBase import cursor,conn
router=APIRouter()

@router.post("/create_user",status_code=status.HTTP_201_CREATED)
def create_new_user(User_profile:New_User):
    if len(User_profile.email)>65:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Email size cannot be more than 65")
    password=User_profile.password
    new_password=hash(password)
    cursor.execute("""INSERT INTO users (user_name,email,password) VALUES (%s,%s,%s)""",(User_profile.user_name,User_profile.email,new_password))
    cursor.fetchall()
    conn.commit()
    return "post created successfully"


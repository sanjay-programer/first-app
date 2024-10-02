from fastapi import APIRouter,HTTPException,status
from app.DataBase import cursor,conn
from app import schemas

router=APIRouter(
    tags=['POST']
)

@router.get("/")
def root():
    return "Hello world"

@router.get("/all_post")
def getting_all_post():
    cursor.execute("""SELECT * FROM my_post""")
    post=cursor.fetchall()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no post were found")
    else:
        return schemas.post_control.from_db_list(post)

@router.post("/create_post",status_code=status.HTTP_201_CREATED)
def creating_new_post(post:schemas.create_post):
    #validtaing if owner present
    cursor.execute("""SELECT * FROM users WHERE user_id=%s""",(post.owner_id,))
    val=cursor.fetchall()
    if not val:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"no user with id: {post.owner_id}")

    #validating the length of title and content
    if len(post.title)>45:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Title size cannot be more than 45 length ")

    if len(post.content)>190:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Content size cannot be more than 190 length ")
    cursor.execute("""INSERT INTO my_post(title,content,is_published,owner_id) VALUES (%s,%s,%s,%s)""",(post.title,post.content,post.is_published,post.owner_id))
    new_post=cursor.fetchall()
    conn.commit()
    if new_post==None:
        return "error"
    else:
        return "post created successfully"

@router.put("/update_post/{post_id}")
def updating_post(post_id,updated_post:schemas.POST):
    cursor.execute("""SELECT * FROM my_post WHERE id =%s""",(post_id,))
    post_existence=cursor.fetchall()
    if not post_existence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")

    if len(updated_post.title)>45:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Title size cannot exceed 45")

    if len(updated_post.content)>190:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"Content size cannot exceed 190")

    cursor.execute("""UPDATE my_post SET title = %s,content=%s,is_published=%s WHERE id=%s""",
                   (updated_post.title,updated_post.content,updated_post.is_published,post_id))
    conn.commit()
    return "post updated successfully"

@router.delete("/delete_post/{deleting_id}")
def deleting_post(deleting_id:int):
    cursor.execute("""SELECT * FROM my_post WHERE id =%s""",(deleting_id,))
    post_existence=cursor.fetchall()
    if not post_existence:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {deleting_id} not found")
    cursor.execute("""DELETE FROM my_post WHERE id=%s""",(deleting_id,))
    conn.commit()
    return f"post deleted successfully"

@router.get("/get_post/{post_id}",response_model=schemas.post_control)
def geting_post(post_id):
    cursor.execute("""SELECT * FROM my_post WHERE id=%s""",(post_id,))
    post=cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    return schemas.post_control.from_db(post)

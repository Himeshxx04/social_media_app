from starlette import status
from passlib.exc import UsedTokenError
from .. import models,schemas,oauth2
from fastapi import HTTPException,Depends,FastAPI,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user),limit:int=10,skip:int=0,search:Optional[str]=""):
      #cursor.execute('SELECT * FROM "Posts"')
        #posts = cursor.fetchall()
        print(limit)
        posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        return  posts
    
     
     




@router.post("/",response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
     #cursor.execute(""" INSERT INTO "Posts"(title,content,published) VALUES(%s,%s,%s) RETURNING*""",(new_post.title,new_post.content,new_post.published) )
        #post_new=cursor.fetchone()
        #conn.commit()

        print(current_user.email)
        posts_dict=new_post.model_dump()
        posts_dict.update({"user_id":current_user.id})
        post_new=models.Post(**posts_dict)
     
        db.add(post_new)
        db.commit()
        db.refresh(post_new)
        
        return post_new
    
       
    


@router.get("/{id}",response_model=schemas.Post)
def get_post(id: int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    individual_post=db.query(models.Post).filter(models.Post.id==id).first()
   
    if individual_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return  individual_post

    
       
   
    

@router.delete("/{id}")
def delete_post(id: int,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
    deleted_post=db.query(models.Post).filter(models.Post.id==id).first()
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    if deleted_post.user_id!=current_user.id:
        raise HTTPException(status_code=401,detail="not authorized to perform the task")
    db.delete(deleted_post)
    db.commit()
    return {"message":"post deleted"}
   


     

@router.put("/{id}",response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int=Depends(oauth2.get_current_user)):
    
        ##cursor.execute("""UPDATE "Posts" set title=%s,content=%s,published=%s where id=%s RETURNING *""",(updated_post.title,updated_post.content,updated_post.published,id,) )
        ##updated_post=cursor.fetchone()
        ##conn.commit()
        updated_query=db.query(models.Post).filter(models.Post.id==id)
        updated_post=updated_query.first()
        if updated_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        if updated_post.user_id!=current_user.id:
            raise HTTPException(status_code=401,detail="not authorized to perform requested action")
        
        updated_query.update(post.model_dump())
        db.commit()
        
        return updated_query.first()


   
'''@app.put("/posts/{id}")
def update_post(id: int, updated_post: Posts):
    try:
        cursor.execute("""UPDATE "Posts" set title=%s,content=%s,published=%s where id=%s RETURNING *""",(updated_post.title,updated_post.content,updated_post.published,id,) )
        updated_post=cursor.fetchone()
        conn.commit()
        if updated_post is None:
            raise HTTPException(status_code=404, detail="Post not found")
        return {"updated_post":updated_post}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))'''
    
    

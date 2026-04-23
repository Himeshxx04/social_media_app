from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends,FastAPI,APIRouter

from ..import models,schemas,oauth2,database


router=APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/")
def create_vote(vote:schemas.Vote,db:Session=Depends(database.get_db),current_user:int=Depends(oauth2.get_current_user)):
    post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f"Post with id {vote.post_id} does not exist")
    vote_query=db.query(models.Votes).filter(models.Votes.post_id==vote.post_id,models.Votes.user_id==current_user.id)
    current_vote=vote_query.first()
    if vote.vote_dir==1:
        if current_vote:
            raise HTTPException(status_code=409,detail=f"Post{vote.post_id} has already been voted by {current_user.id}")
      
        vote_new=models.Votes(post_id=vote.post_id,user_id=current_user.id)
        db.add(vote_new)
        db.commit()
        return{"message":"Vote Created successfully"}
    else:
        if current_vote is None:
            raise HTTPException(status_code=404,detail="Not found")
        db.delete(current_vote)
        db.commit()
        return{"message":"Vote Deleted Successfully"}


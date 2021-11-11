from fastapi import status, Response, HTTPException, Depends, APIRouter
from .. import schema, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/vote',
    tags=['Vote']
)

@router.post("/", status_code = status.HTTP_201_CREATED)
def vote(vote: schema.vote, db: Session = Depends(database.get_db), current_user: models.User = Depends
(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="The user has already voted to the post")
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)

            return {'message': 'Voted Succesfully'}
    else:

        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="vote does not exist")
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {'message': 'Removed the vote succesfully'}
        
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, File, UploadFile
from devmodule.core import schemas, database, models
from devmodule.repository import project


# To add review to a project with validations
def add_review(proj_id,request,db, current_user):
    curr_project_review = project.get_project_review(proj_id,db)
    projectObj = project.view_single_project(proj_id,db)
    if current_user.id == projectObj.owner.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You Cannot add review to your own project")
    elif curr_project_review:
        for review in curr_project_review:
            if review.owner is current_user:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You have already added your review")  
        else:
            return add_review_to_db(proj_id,request,db, current_user)
    else:
        return add_review_to_db(proj_id,request,db, current_user)

# To add review to db project 
def add_review_to_db(proj_id,request,db, current_user):
    create_review = models.Review(
        comment = request.comment,
        vote_value =request.vote_value,
        project_id = proj_id,
        owner_id = current_user.id
    )
    db.add(create_review)
    db.commit()
    db.refresh(create_review)
    update_vote_count(proj_id,db)
    vote_ratio = get_positive_feedback(proj_id,db)
    update_vote_ratio(proj_id,vote_ratio,db)

    return create_review

# To return all the reviews
def view_all_review(db):
    reviews = db.query(models.Review).all()
    return reviews

# To update the vote count in projects table
def update_vote_count(proj_id,db):
    projectObj = db.query(models.Project).filter(models.Project.id == proj_id)
    vote_update = {
        'vote_total':projectObj.first().vote_total+1
    }
    projectObj.update(vote_update)
    db.commit()
    return "updated"

# To update the vote ratio in projects table
def update_vote_ratio(proj_id,vote_ratio,db):
    projectObj = db.query(models.Project).filter(models.Project.id == proj_id)
    vote_ratio_update = {
        'vote_ratio':round(vote_ratio,2)
    }
    projectObj.update(vote_ratio_update)
    db.commit()
    return "updated"

# To get the positive votes from all the votes
def get_positive_feedback(project_id,db):
    project = db.query(models.Project).filter(models.Project.id == project_id).first()
    reviews = db.query(models.Review).filter(models.Review.project_id == project_id).all()
    up_votes = 0
    for review in reviews:
        if review.vote_value == 'up':
            up_votes += 1
    total_votes = project.vote_total
    vote_ratio = (up_votes/total_votes)*100
    return vote_ratio


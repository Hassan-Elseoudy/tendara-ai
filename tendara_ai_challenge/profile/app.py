from datetime import datetime

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from tendara_ai_challenge.matching.alchemy import Profile, create_db_and_tables, get_session
from tendara_ai_challenge.profile.dto import SearchProfileRequestSchema, SearchProfileResponseSchema

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.post("/profiles", response_model=SearchProfileResponseSchema)
async def create_profile(*, session: Session = Depends(get_session), profile: SearchProfileRequestSchema):
    db_profile = Profile(
        location_id=profile.location_id,
        category_id=profile.category_id,
        tag_ids=",".join(map(str, profile.tag_ids)),
        # TODO: Add publication_deadline to the Profile object.
        publication_deadline=datetime.max
    )
    session.add(db_profile)
    session.commit()
    session.refresh(db_profile)

    # TODO: Moving to dedicated mapping Model.
    response_data = {
        "id": db_profile.id,
        "category_id": db_profile.category_id,
        "location_id": db_profile.location_id,
        "tags": list(map(int, db_profile.tag_ids.split(","))),
        "publication_deadline": db_profile.publication_deadline
    }

    # TODO: Return the result in HTTP Response.
    return SearchProfileResponseSchema(**response_data)


@app.get("/profiles/{id}", response_model=SearchProfileResponseSchema)
async def get_profile(id: int, session: Session = Depends(get_session)):
    profile = session.query(Profile).filter_by(id=id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    # TODO: Moving to dedicated mapping Model.
    response_data = {
        "id": profile.id,
        "category_id": profile.category_id,
        "location_id": profile.location_id,
        "tags": list(map(int, profile.tag_ids.split(","))),
        "publication_deadline": profile.publication_deadline
    }

    # TODO: Return the result in HTTP Response.
    return SearchProfileResponseSchema(**response_data)


@app.delete("/profiles/{id}")
async def delete_profile(id: int, session: Session = Depends(get_session)):
    profile = session.query(Profile).filter_by(id=id).first()
    if profile is None:
        raise HTTPException(status_code=404, detail="Profile not found")
    session.delete(profile)
    session.commit()

    # TODO: Return the result in HTTP Response.
    return {"message": "Profile deleted successfully"}

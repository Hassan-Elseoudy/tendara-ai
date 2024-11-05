from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from tendara_ai_challenge.matching.dto import MatchingNoticesResponse
from tendara_ai_challenge.matching.entity import Profile, get_session
from tendara_ai_challenge.matching.matching import find_relevant_notices

app = FastAPI()


@app.get("/profiles/{profile_id}/matches", response_model=MatchingNoticesResponse)
async def get_matches(profile_id: int, db: Session = Depends(get_session)):
    profile = db.query(Profile).get(profile_id)

    if profile is None:
        raise HTTPException(status_code=404, detail="User not found")

    matching_notices = find_relevant_notices(profile, db)
    return MatchingNoticesResponse(notices=matching_notices)

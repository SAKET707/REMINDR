from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
# these are shared fastapi dependencies used across app
from core.database import SessionLocal
from core.security import Security
from models.user import User

# this doesnt perform google oauth , it tells fastapi , look for a bearer token in authorization header, fastapi extracts the token and passes it as token
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/google/login",
)
# it doesnt verify jwts only extraction of tokens

# if we didnt have this every endpoint would have this code all over so fastapi says it needs to be at one place once
# u define once then Depends(get_db) means it instructs fastapi that before calling the endpoint execute get_db and give its result
def get_db():

    #create a session
    db = SessionLocal() # write this once not in all endpoints 
    # at places we write  Depends(get_db) and fastapi gives db session automatically , this is called dependency injection

    try:
        yield db # this is python generator. it pauses the func here . if it was return then db would never be closed in next lines
                # after the endpoint finishes execution resumes and finnally runs
    finally:
        db.close() # we need to close them always .suppose we dont and 100 req each opens a session but never returns it to pool.
                    # so connection pool exhausts and new req  get db connection errors . app slows or fails

        # so every req , open db session, run endpoint and close the db session

# this is authentication middleware
# flow is jwt verify , extract user id , find user , return user object
# db is queried becos db checks prevents api acess for deleted users
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:

    try:
        # verify expiry and jwt signature if ok return  decoded payload
        payload = Security.verify_access_token(token)

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

    except JWTError:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = (
        db.query(User)
        .filter(User.id == user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user



# Authentication Flow
#
# Frontend
#     ↓
# Authorization: Bearer <JWT>
#     ↓
# OAuth2PasswordBearer extracts token
#     ↓
# verify_access_token()
#     ↓
# Extract user_id
#     ↓
# Query database
#     ↓
# Return current User object
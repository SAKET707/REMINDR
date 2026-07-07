from sqlalchemy.orm import Session

from models.user import User


def create_or_update_google_user(
    db: Session,
    google_id: str,
    email: str,
    name: str,
    profile_picture: str | None,
    refresh_token: str | None,
):
    user = db.query(User).filter(
        User.google_id == google_id
    ).first()

    if user:
        user.name = name
        user.email = email
        user.profile_picture = profile_picture
        if refresh_token:
            user.encrypted_refresh_token = refresh_token

        db.commit()
        db.refresh(user)

        return user

    user = User(
        google_id=google_id,
        email=email,
        name=name,
        profile_picture=profile_picture,
        encrypted_refresh_token=refresh_token,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user




def get_user_by_email(
    db: Session,
    email: str,
) -> User | None:

    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )
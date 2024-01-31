from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
        Args:
            email (str): The email address of the user to be retrieved.
            db (Session): A connection to a database session.
    
    :param email: str: Get the email of the user
    :param db: Session: Pass the database session to the function
    :return: The first user that has the given email
    :doc-author: Trelent
    """
    return db.query(User).filter_by(email=email).first()


async def create_user(body: UserModel, db: Session):
    """
    The create_user function creates a new user in the database.
        
    
    :param body: UserModel: Get the user's email and username
    :param db: Session: Create a new session with the database
    :return: A user object
    :doc-author: Trelent
    """
    grav = Gravatar(body.email)
    new_user = User(**body.dict(), avatar=grav.get_image())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, refresh_token, db: Session):
    """
    The update_token function updates the user's refresh token in the database.
        Args:
            user (User): The User object to update.
            refresh_token (str): The new refresh token for this user.
            db (Session): A database session to use for updating the User object.
    
    :param user: User: Update the user's refresh token in the database
    :param refresh_token: Update the user's refresh token in the database
    :param db: Session: Pass the database session to the function
    :return: A new refresh token
    :doc-author: Trelent
    """
    user.refresh_token = refresh_token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Get the email address of the user
    :param db: Session: Pass the database session to the function
    :return: None, but the return type is none
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str): The URL for the new avatar image.
        db (Session, optional): A database session object to use instead of creating one locally. Defaults to None.  # noQA: E501 line too long, but this is an example!  # noQA: E501 line too long, but this is an example!  # noQA: E501 line too long, but this is an example!  # noQ
    
    :param email: Find the user in the database
    :param url: str: Specify the type of data that is being passed in
    :param db: Session: Pass the database session into the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user

import os

from sqlalchemy.orm import Session

from hashed_authorizer import create_ftp_user
from paths import assemble_ftp_path
from user import User, engine


def register_user(file):
    """Add a new user to the database"""
    with open(file, 'r') as registration_file:
        user_data = registration_file.read().splitlines()
    os.remove(file)
    if len(user_data) >= 3:
        session = Session(bind=engine)
        user = User(user_data[0], user_data[1], user_data[2])
        session.add(user)
        session.commit()
        create_homedir(user)
        create_ftp_user(user)
    else:
        pass  # TODO: Log/create warning


def create_homedir(user):
    """Create the user's home directory"""
    os.mkdir(assemble_ftp_path('users', user.name))
    os.mkdir(assemble_ftp_path('users', user.name, 'posts'))
    os.mkdir(assemble_ftp_path('users', user.name, 'feed'))

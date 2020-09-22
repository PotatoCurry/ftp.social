import os

from pyftpdlib.handlers import TLS_FTPHandler
from sqlalchemy.orm import Session

from registration import register_user
from user import engine, User


class CustomHandler(TLS_FTPHandler):
    def on_file_received(self, file):
        """Checks if the file uploaded was a post, following list, or registration"""
        file_info = file.split(os.sep)
        filename = file_info[-1]
        directory = file_info[-2]
        session = Session(bind=engine)
        user = session.query(User).filter_by(name=self.username).first()
        session.commit()
        if directory == 'posts':  # User uploads a new post
            user.distribute_post(file)
        elif self.username == directory and filename == 'following.txt':  # User updates their following list
            user.update_following(file)
        elif directory == 'registration':
            register_user(file)

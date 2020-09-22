import os
import re
from datetime import date

from passlib.handlers.bcrypt import bcrypt
from sqlalchemy import Column, Integer, String, Table, ForeignKey, UniqueConstraint, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

from paths import assemble_ftp_path

engine = create_engine(os.environ["FTPSOCIAL_DATABASE_URL"], echo=True)
Base = declarative_base()
user_followers = Table('user_followers', Base.metadata,
                       Column('user_id', ForeignKey('users.id'), index=True),
                       Column('follower_id', ForeignKey('users.id')),
                       UniqueConstraint('user_id', 'follower_id', name='unique_follows'))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    email = Column(String(90), unique=True)
    password = Column(String(60), nullable=False)

    followers = relationship('User',
                             back_populates='following',
                             secondary=user_followers,
                             primaryjoin=id == user_followers.columns.follower_id,
                             secondaryjoin=id == user_followers.columns.user_id,
                             foreign_keys=[id])
    following = relationship('User',
                             back_populates='followers',
                             secondary=user_followers,
                             primaryjoin=id == user_followers.columns.follower_id,
                             secondaryjoin=id == user_followers.columns.user_id,
                             foreign_keys=[id])

    def __init__(self, username, email, password):
        self.name = username
        self.email = email
        self.password = bcrypt.hash(password)

    def follow(self, user):
        """Follow the specified user"""
        conn = engine.connect()
        ins = user_followers.insert().values(user_id=user.id, follower_id=self.id)
        conn.execute(ins)

    def unfollow(self, user):
        """Unfollow the specified user"""
        conn = engine.connect()
        rem = user_followers.delete().values(user_id=user.id, follower_id=self.id)
        conn.execute(rem)

    def unfollow_all(self):
        """Unfollow all users"""
        conn = engine.connect()
        rem = user_followers.delete().where(user_followers.c.follower_id == self.id)
        conn.execute(rem)

    def distribute_post(self, file):
        """Distribute the file to the user's followers' feeds"""
        filename = os.path.basename(file)
        if date_stamp := re.match(r'\d{4}\.\d{2}\.\d{2}', filename):  # User edited an existing post with a date stamp
            dot_date = date_stamp.group()
            dated_file = file
            dated_filename = filename
            name_start = date_stamp.span()[1] + 1  # Where the original name of the file starts
            pure_filename = dated_filename[name_start:]  # Cut off date from filename
        else:  # User uploaded a new post with no date stamp
            dot_date = date.today().strftime('%Y.%m.%d')  # Dotted and padded date pattern, e.g. 2020.07.18
            dated_filename = dot_date + '.' + filename
            dated_file = assemble_ftp_path('users', self.name, 'posts', dated_filename)
            os.replace(file, dated_file)
            pure_filename = filename
        stamped_filename = '.'.join([dot_date, self.name, pure_filename])

        for user in self.followers:
            feed_file = assemble_ftp_path('users', user.name, 'feed', stamped_filename)
            # shutil.copy2(dated_file, feed_file)  Copy file
            os.link(dated_file, feed_file)  # Create hard link from follower feed to original post

    def update_following(self, file):
        """Update the user's following list"""
        self.unfollow_all()
        with open(file) as following_file:
            following_list = following_file.read().splitlines()
        session = Session(bind=engine)
        for username in following_list:
            following_user = session.query(User).filter_by(name=username).first()
            if following_user is not None:  # Ignore nonexistent users
                self.follow(following_user)

    def __repr__(self):
        return "<User(id ='%d', name='%s', email='%s')>" % (self.id, self.name, self.email)

from passlib.handlers.bcrypt import bcrypt
from pyftpdlib.authorizers import AuthenticationFailed, DummyAuthorizer
from sqlalchemy.orm import Session

from paths import base_dir, assemble_ftp_path
from user import User, engine


class HashedAuthorizer(DummyAuthorizer):
    """Authorizer compatible with hashed passwords"""
    def validate_authentication(self, username, password, handler):
        """Validate authentication with hashed password"""
        msg = "Authentication failed."
        if not self.has_user(username):
            raise AuthenticationFailed(msg)
        if username != 'anonymous':
            if not bcrypt.verify(password, self.user_table[username]['pwd']):
                raise AuthenticationFailed(msg)

    def _check_permissions(self, username, perm):
        """Removed write permissions assigned to anonymous user warning"""
        for p in perm:
            if p not in self.read_perms + self.write_perms:
                raise ValueError('no such permission %r' % p)


authorizer = HashedAuthorizer()


def create_authorizer():
    """Returns an authorizer with accounts for users in the database"""
    authorizer.add_anonymous(base_dir)  # Read-only access to the full server
    authorizer.override_perm('anonymous', assemble_ftp_path('registration'), 'elw', True)  # Write-only access to registration
    session = Session(bind=engine)
    for user in session.query(User).all():
        create_ftp_user(user)
    return authorizer


def create_ftp_user(user):
    """Adds a user to the FTP authorizer"""
    authorizer.add_user(user.name, user.password, base_dir)  # Read-only access to the full server
    authorizer.override_perm(user.name, assemble_ftp_path('registration'), '', True)  # No access to registration
    authorizer.override_perm(user.name, assemble_ftp_path('users', user.name, 'feed'), 'elr', True)  # Read-only feeds
    authorizer.override_perm(user.name, assemble_ftp_path('users', user.name), 'elradfmw', True)  # Full perms in homedir

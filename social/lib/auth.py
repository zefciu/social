from zope.interface import implements
from repoze.who.interfaces import IAuthenticator
from social.model import Session, User
from sqlalchemy.orm.exc import NoResultFound

class SocialPlugin(object):
    implements(IAuthenticator)

    def authenticate(self, environ, identity):
        if identity.has_key('login'):
            try:
                user = Session.query(User).filter(
                    User.login == identity['login']
                ).one()
            except NoResultFound:
                return
            if user.check_passwd(identity['passwd']):
                return user.login

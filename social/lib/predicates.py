from repoze.what.predicates import Predicate
from social.model import Session, User
from sqlalchemy.orm.exc import NoResultFound

class is_friend(Predicate):
    message = "User must be a friend to do it"
    def __init__(self, username, *args, **kwargs):
        self.username = username
        super(is_friend, self).__init__(*args, **kwargs)

    def evaluate(self, environ, credentials):
        print credentials, self.username
        if credentials['repoze.what.userid'] == self.username:
            return # It's always ok to view your own data
        try:
            user = Session.query(User).filter(
                User.login == credentials['repoze.what.userid']
            ).one()
        except NoResultFound:
            self.unmet()
            
        if self.username in [u.login for u in user.friends]:
            return
        
        if self.username in [u.login for u in user.back_friends]:
            return

        self.unmet()

"""The application's model objects"""
from social.model.meta import Session, metadata
import sqlalchemy as sa
from sqlalchemy import orm
import string
import random as rnd
from base64 import b64encode
from hashlib import sha512

friendships_table = sa.Table(
    'friendships', metadata,
    sa.Column(
        'requester_id', sa.types.Integer(), sa.ForeignKey('users.id'),
        primary_key = True
    ),
    sa.Column('acceptor_id', sa.types.Integer(), sa.ForeignKey('users.id'),
              primary_key = True
             ),
    sa.Column('accepted', sa.types.Boolean()),
)

users_table = sa.Table(
    'users', metadata,
    sa.Column(
        'id', sa.types.Integer, sa.schema.Sequence(
            'users_id_seq', optional= True
        ), primary_key = True
    ),
    sa.Column('login', sa.types.String(32)),
    sa.Column('hash', sa.types.String(88)),
    sa.Column('salt', sa.types.String(12)),
)

class Friendship(object):
    def __init__(self, requester_id, acceptor_id):
        self.requester_id = requester_id
        self.acceptor_id = acceptor_id
        self.accepted = False

class User(object):
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd

    passwd = property()
    @passwd.setter
    def passwd(self, passwd):
        self.salt = ''.join((rnd.choice(string.printable) for i in range(12)))
        self.hash = b64encode(sha512(passwd + self.salt).digest())

    def check_passwd(self, passwd):
        return self.hash == b64encode(sha512(passwd + self.salt).digest())

orm.mapper(User, users_table, properties = {
    'friends': orm.relationship(
        User, secondary = friendships_table, 
        primaryjoin = (
            (friendships_table.c.requester_id == users_table.c.id) &
            (friendships_table.c.accepted == True)
        ), secondaryjoin = (
            friendships_table.c.acceptor_id == users_table.c.id
        ), backref = 'back_friends')
})

orm.mapper(Friendship, friendships_table, properties = {
    'requester': orm.relationship(User, primaryjoin = (
        (friendships_table.c.requester_id == users_table.c.id) &
        (friendships_table.c.accepted == False)
    )),
    'acceptor': orm.relationship(User, primaryjoin = (
        (friendships_table.c.acceptor_id == users_table.c.id) &
        (friendships_table.c.accepted == False)
    ))
})

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

"""The application's model objects"""
from social.model.meta import Session, metadata
import sqlalchemy as sa
from sqlalchemy import orm
import string
import random as rnd
from base64 import b64encode
from hashlib import sha512

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

orm.mapper(User, users_table)

def init_model(engine):
    """Call me before using any of the tables or classes in the model"""
    Session.configure(bind=engine)

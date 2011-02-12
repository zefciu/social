#vim: set fileencoding=utf-8
import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import validate
import formencode as fe

from social.lib.base import BaseController, render
from social.model import Session, User

from repoze.who.api import get_api

log = logging.getLogger(__name__)

class LoginValidator(fe.FancyValidator):
    messages = {
        'too_few': unicode('Podany login jest za krótki', 'utf-8'),
        'too_many': unicode('Podany login jest za dlugi', 'utf-8'),
        'taken': unicode('Podany login jest juz zajęty', 'utf-8'),
    }
    def validate_python(self, value, state):
        if len(value) > 32:
            raise fe.Invalid(self.message(
                'too_many', state),
                value, state
            )
        if len(value) < 3:
            raise fe.Invalid(self.message('too_few', state),
                value, state
            )
        if Session.query(User).filter(User.login == value).count():
            raise fe.Invalid(self.message('taken', state),
                value, state
            )


class RegisterSchema(fe.Schema):
    login = LoginValidator()
    passwd = fe.validators.String(min = 7)
    repeatPasswd = fe.validators.String()
    chained_validators = [fe.validators.FieldsMatch('passwd', 'repeatPasswd')]

class UsersController(BaseController):

    def welcome(self):
        if not request.environ.has_key('REMOTE_USER'):
            abort(401)
        else:
            c.username = request.environ['REMOTE_USER']
            return render('/users/welcome.mako')

    @validate(schema = RegisterSchema, form = 'register')
    def register(self):
        if hasattr(self, 'form_result'):
            user = User(self.form_result['login'], self.form_result['passwd'])
            Session.add(user)
            Session.commit()
            redirect('/')
        else:
            return render('/users/register.mako')

    def login(self):
        c.message = ''
        who_api = get_api(request.environ)
        if 'login' in request.POST:
            authenticated, headers = who_api.login({
                'login': request.POST['login'],
                'passwd': request.POST['passwd'],
            })
            if authenticated:
                response.headers = headers
                return redirect('/')
            c.message = 'Zły login lub hasło'
        else:
             # Forcefully forget any existing credentials.
             authenticated, headers = who_api.login({})
 
        if 'REMOTE_USER' in request.environ:
            del request.environ['REMOTE_USER']

        return render('/users/login.mako')

    def logout(self):
        who_api = get_api(request.environ)
        response.headers = who_api.forget()
        return redirect('/login')

import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from social.lib.base import BaseController, render

log = logging.getLogger(__name__)

class FriendshipsController(BaseController):

    def index(self):
        # Return a rendered template
        #return render('/friendships.mako')
        # or, return a response
        return 'Hello World'

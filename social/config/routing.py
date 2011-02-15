"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from routes import Mapper

def make_map(config):
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])
    map.minimization = False
    map.explicit = False

    # The ErrorController route (handles 404/500 error pages); it should
    # likely stay at the top, ensuring it can always be resolved
    map.connect('/error/{action}', controller='error')
    map.connect('/error/{action}/{id}', controller='error')

    # CUSTOM ROUTES HERE
    map.connect('/', controller = 'users', action = 'welcome')
    map.connect('/login', controller = 'users', action = 'login')
    map.connect('/logout', controller = 'users', action = 'logout')
    map.connect('/register', controller = 'users', action = 'register')
    map.connect('/user/{login}', controller = 'users', action = 'display')
    map.connect('/befriend/{login}', controller = 'users', action = 'befriend')

    map.connect('/{controller}/{action}')
    map.connect('/{controller}/{action}/{id}')

    return map

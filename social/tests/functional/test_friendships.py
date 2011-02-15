from social.tests import *

class TestFriendshipsController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='friendships', action='index'))
        # Test response...

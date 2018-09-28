"""
Custom Github authenticator
"""
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator

class GitHubOAuthenticator(_GitHubOAuthenticator):

    def authenticate(self, handler, data=None):
        r = super().authenticate(handler, data)
        self.log.info("!!!! authenticate {}".format(r))
        return r

    def get_authenticated_user(self, handler, data):
        r = super().get_authenticated_user(handler, data)
        self.log.info("!!!! get_authenticated_user {}".format(r))
        return r

    def check_whitelist(self, username):
        r = super().check_whitelist(username)
        self.log.info("!!!! check_whitelist {}".format(r))
        return r




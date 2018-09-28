"""
Custom Github authenticator
"""
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator

class GitHubOAuthenticator(_GitHubOAuthenticator):

    def authenticate(self, handler, data=None):
        r = super().authenticate(handler, data)
        self.log.warning("!!!! authenticate", r)
        return r

    def get_authenticated_user(self, handler, data):
        r = super().get_authenticated_user(handler, data)
        self.log.warning("!!!! get_authenticated_user", r)
        return r

    def check_whitelist(self, username):
        r = super().check_whitelist(username)
        self.log.warning("!!!! check_whitelist", r)
        return r




"""
Custom Github authenticator
"""
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator
from tornado import gen, web

class GitHubOAuthenticator(_GitHubOAuthenticator):


    def check_whitelist(self, username):
        r = super().check_whitelist(username)
        self.log.info("!!!! check_whitelist {} {}".format(username, r))
        return r




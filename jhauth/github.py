"""
Custom Github authenticator
"""
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator

import requests
from os import getenv
import re

class GitHubOAuthenticator(_GitHubOAuthenticator):


    def check_whitelist(self, username):
        """Check that the username is in an access list stored at Github"""


        url = getenv('JUPYTER_GITHUB_ACCESS_LIST')

        if not url:
            raise Exception()

        lines = [re.sub('\#.*', '', e).strip() for e in requests.get(url).text.splitlines()]

        lines = [l for l in lines if l] # Remove blanks

        if username in lines:
            return

        if 'anyone' in lines or '*' in lines:
            return True

        return False




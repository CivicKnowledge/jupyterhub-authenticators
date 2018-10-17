"""
Custom Github authenticator
"""
import json
import re
import requests
from oauthenticator.common import next_page_from_links
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator
from oauthenticator.github import _api_headers, GITHUB_API, GITHUB_PROTOCOL
from os import getenv
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient


class GitHubOAuthenticator(_GitHubOAuthenticator):

    def x_check_whitelist(self, username):
        """Check that the username is in an access list stored at Github"""


        url = getenv('JUPYTER_GITHUB_ACCESS_LIST')

        if not url:
            raise Exception()

        lines = [re.sub('\#.*', '', e).strip() for e in requests.get(url).text.splitlines()]

        lines = [l for l in lines if l] # Remove blanks

        if username in lines:
            return True

        if 'anyone' in lines or '*' in lines:
            return True

        return False


    @gen.coroutine
    def _check_organization_whitelist(self, org, username, access_token):
        http_client = AsyncHTTPClient()
        headers = _api_headers(access_token)
        # Get all the members for organization 'org'
        # With empty scope (even if authenticated by an org member), this
        #  will only yield public org members.  You want 'read:org' in order
        #  to be able to iterate through all members.
        next_page = "%s://%s/orgs/%s/members" % (GITHUB_PROTOCOL, GITHUB_API, org)
        while next_page:
            req = HTTPRequest(next_page, method="GET", headers=headers)
            resp = yield http_client.fetch(req)
            resp_json = json.loads(resp.body.decode('utf8', 'replace'))
            next_page = next_page_from_links(resp)
            for entry in resp_json:
                self.log.warning('XXX {} {} '.format(org,str(entry)))
                if username == entry['login']:
                    return True

        return False

def pre_spawn_hook(spawner):
    spawner.log.warn("!!!! HOOK FOR SPAWNER")
    spawner.log.warn(spawner.args)
    spawner.log.warn(spawner.user_options)


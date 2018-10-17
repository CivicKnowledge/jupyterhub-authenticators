"""
Custom Github authenticator
"""
import json
import re
import requests
from oauthenticator.common import next_page_from_links
from oauthenticator.github import GitHubOAuthenticator as _GitHubOAuthenticator
from oauthenticator.github import _api_headers, GITHUB_API, GITHUB_PROTOCOL, GITHUB_HOST
from os import getenv
from tornado import gen
from tornado.httpclient import HTTPRequest, AsyncHTTPClient
from tornado.httpclient import HTTPRequest, AsyncHTTPClient, HTTPError
from tornado.httputil import url_concat

class GitHubOAuthenticator(_GitHubOAuthenticator):


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
                #self.log.warning('XXX {} {} '.format(org,str(entry)))
                if username == entry['login']:
                    return True

        return False



async def pre_spawn_hook(spawner):

    spawner.log.warn("!!!! HOOK FOR SPAWNER")
    spawner.log.warn("!!!! AUTH State")

    try:
        spawner.log.warn("A1 "+str(spawner.authenticator))
    except Exception as e:
        spawner.log.warn("NOPE "+str(e))

    try:
        auth_state = spawner.user.auth_state
        spawner.log.warn("A2 "+str(auth_state))
    except Exception as e:
        spawner.log.warn("NOPE "+str(e))

    try:
        from time import sleep

        auth_state = await spawner.user.get_auth_state()
        spawner.log.warn("A3 "+str(auth_state))


    except Exception as e:
        spawner.log.warn("NOPE"+str(e))



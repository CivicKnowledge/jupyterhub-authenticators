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
                #self.log.warning('XXX {} {} '.format(org,str(entry)))
                if username == entry['login']:
                    return True

        return False

    @gen.coroutine
    def authenticate(self, handler, data=None):
        """We set up auth_state based on additional GitHub info if we
        receive it.
        """
        code = handler.get_argument("code")
        # TODO: Configure the curl_httpclient for tornado
        http_client = AsyncHTTPClient()

        # Exchange the OAuth code for a GitHub Access Token
        #
        # See: https://developer.github.com/v3/oauth/

        # GitHub specifies a POST request yet requires URL parameters
        params = dict(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code
        )

        url = url_concat("%s://%s/login/oauth/access_token" % (GITHUB_PROTOCOL, GITHUB_HOST),
                         params)

        req = HTTPRequest(url,
                          method="POST",
                          headers={"Accept": "application/json"},
                          body=''  # Body is required for a POST...
                          )

        resp = yield http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        if 'access_token' in resp_json:
            access_token = resp_json['access_token']
        elif 'error_description' in resp_json:
            raise HTTPError(403,
                "An access token was not returned: {}".format(
                    resp_json['error_description']))
        else:
            raise HTTPError(500,
                "Bad response: %s".format(resp))

        # Determine who the logged in user is
        req = HTTPRequest("%s://%s/user" % (GITHUB_PROTOCOL, GITHUB_API),
                          method="GET",
                          headers=_api_headers(access_token)
                          )
        resp = yield http_client.fetch(req)
        resp_json = json.loads(resp.body.decode('utf8', 'replace'))

        username = resp_json["login"]
        # username is now the GitHub userid.
        if not username:
            return None
        # Check if user is a member of any whitelisted organizations.
        # This check is performed here, as it requires `access_token`.
        if self.github_organization_whitelist:
            for org in self.github_organization_whitelist:
                user_in_org = yield self._check_organization_whitelist(org, username, access_token)
                if user_in_org:
                    break
            else:  # User not found in member list for any organisation
                self.log.warning("User %s is not in org whitelist", username)
                return None
        userdict = {"name": username}
        # Now we set up auth_state
        userdict["auth_state"] = auth_state = {}
        # Save the access token and full GitHub reply (name, id, email) in auth state
        # These can be used for user provisioning in the Lab/Notebook environment.
        # e.g.
        #  1) stash the access token
        #  2) use the GitHub ID as the id
        #  3) set up name/email for .gitconfig
        auth_state['access_token'] = access_token
        # store the whole user model in auth_state.github_user
        auth_state['github_user'] = resp_json
        # A public email will return in the initial query (assuming default scope).
        # Private will not.

        self.log.warning('XXX {}'.format(userdict))

        return userdict


async def pre_spawn_hook(spawner):

    spawner.log.warn("!!!! HOOK FOR SPAWNER")
    spawner.log.warn("!!!! AUTH State")

    try:

        spawner.log.warn("A1 "+str(spawner.user.encrypted_auth_state))
    except Exception as e:
        spawner.log.warn("NOPE"+str(e))


    try:
        from time import sleep
        import IOLoop
        auth_state = IOLoop.current().run_sync(spawner.user.get_auth_state)
        spawner.log.warn("A2 "+str(auth_state))


    except Exception as e:
        spawner.log.warn("NOPE"+str(e))

    try:
        from time import sleep

        auth_state = await spawner.user.get_auth_state()
        spawner.log.warn("A3 "+str(auth_state))


    except Exception as e:
        spawner.log.warn("NOPE"+str(e))



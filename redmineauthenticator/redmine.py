import requests
import json
from requests.auth import HTTPBasicAuth

from traitlets import Unicode

from jupyterhub.auth import Authenticator

from tornado import gen

import os

class RedmineAuthenticator(Authenticator):
    password = Unicode(
        None,
        allow_none=True,
        config=True,
        help="""
        Set a global password for all users wanting to log in.

        This allows users with any username to log in with the same static password.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        
        url= '{}/users/current.json'.format(os.environ['REDMINE_URL'] )

        headers = {'Content-type': 'application/json'}

        print('AUTH!', data['username'], data['password'])

        try:
            r = requests.get(url , auth=HTTPBasicAuth(data['username'], data['password']), headers=headers)
            r.raise_for_status()
            return data['username']
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return None
            else:
                return None
 
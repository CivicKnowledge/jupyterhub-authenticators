import requests
import json
from requests.auth import HTTPBasicAuth

from traitlets import Unicode

from jupyterhub.auth import Authenticator

from tornado import gen

import os

class RedmineAuthenticator(Authenticator):
    
    redmine_url = Unicode(
        os.environ.get('REDMINE_URL', None) ,
        allow_none=True,
        config=True,
        help="""
        Url for the Redmine instance.
        """
    )

    @gen.coroutine
    def authenticate(self, handler, data):
    
        assert self.redmine_url
        
        url= '{}/users/current.json'.format(self.redmine_url)

        headers = {'Content-type': 'application/json'}

        try:
            r = requests.get(url , auth=HTTPBasicAuth(data['username'], data['password']), headers=headers)
            r.raise_for_status()
            return data['username']
           
                
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                return None
            else:
                return None
 
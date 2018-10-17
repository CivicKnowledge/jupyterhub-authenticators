"""
Docker spawner that keeps state.
"""

from dockerspawner.dockerspawner import DockerSpawner as _DockerSpawner
from traitlets import Dict, Unicode, Bool, Int, Any, default, observe
import uuid

class DockerSpawner(_DockerSpawner):

    key = Unicode(uuid.uuid4().hex)

    def get_state(self):
        state = super().get_state()
        state['key'] = self.key
        return state

    def load_state(self, state):
        print("Loading state", state)
        if 'key' in state:
            self.key = state['key']
        super().load_state(state)




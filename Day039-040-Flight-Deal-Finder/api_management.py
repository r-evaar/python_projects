import requests
import os
import json

class APIManager:

    NUM_OBJ = 0

    def __init__(self, ep, key, key_name='apikey', simulate=True):
        self.ep = ep
        self.key = key
        self.simulate = simulate
        self.NUM_OBJ += 1
        self.cache_filename = \
            f"{self.__class__.__name__}_{self.NUM_OBJ:05d}.json"
        self.headers = {
            f'{key_name}': key
        }

    def get(self, query=None, verbose=False):
        if self.simulate and os.path.isfile(self.cache_filename):
            with open(self.cache_filename, 'r') as f:
                response = json.load(f)
        else:
            response = requests.get(url=self.ep, params=query, headers=self.headers)
            response.raise_for_status()
            response = response.json()

            if verbose:
                print(response)

        if self.simulate:
            with open(self.cache_filename, 'w') as f:
                json.dump(response, f, indent=4)

        return response

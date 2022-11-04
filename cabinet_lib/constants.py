import os
import pdb

ENV = os.getenv('ENV')

def get_url(env):
    if env == 'dev_local' or env=='testing':
        url = 'http://localhost:5050'
    else: #remote
        url = "https://..."
    return url

ROOT_URL = get_url(ENV)
import pdb
import json
from typing import List
import os
from shutil import copyfile 
from hashlib import sha256

import yaml


def get_root_url()->str:
    ENV = 'dev_local'
    if os.getenv('ENV'):
        ENV = os.getenv('ENV')
    with open('config/config.yaml', 'r') as f:
        config_dict = yaml.safe_load(f)
    root_url = config_dict['cabinet'][ENV]
    return root_url


def encode_blob(file_path:str) ->str:
    """
    Takes file path to blob and converts blob to base64 encoded string
    """
    with open(file_path, mode='rb') as f:
        blob_bytes = f.read()
    blob_hash = sha256(blob_bytes).hexdigest()
    return blob_hash

def save_blob(file_path: str, paths) -> bool:
    try:
        # save file to cabinet locations
        for path in paths:
            copyfile(file_path, path)
    except IOError as e:
        raise Exception('unable to copy file %s' % e)
    except Exception:
        raise Exception('Problem saving blob')
    return True


def bytify(base64_str: str) ->bytes: 
    blob_b64_bytes = base64_str.encode('ascii')
    blob_bytes = base64.b64decode(blob_b64_bytes) 
    return blob_bytes 


def make_url(blob_type:str, parameters:dict) -> str:
    if not blob_type in parameters.keys():
        parameters['blob_type'] = blob_type
    url = "/blob?"
    for key in parameters:
        url += f'{key}={parameters[key]}&'
    url = url[0:-1] 
    return url






import pdb
import json
import base64
import os

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
    blob_base64 = base64.b64encode(blob_bytes)
    blob_b64s = blob_base64.decode('ascii')
    return blob_b64s


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






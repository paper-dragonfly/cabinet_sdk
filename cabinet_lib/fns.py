import json
import pdb
import requests
import base64

import psycopg2
import yaml

from cabinet_lib.constants import ROOT_URL



def encode_blob(file_path:str) ->str:
    """
    Takes file path to blob and converts blob to base64 encoded string
    """
    with open(file_path, mode='rb') as f:
        blob_bytes = f.read()
    blob_base64 = base64.b64encode(blob_bytes)
    blob_b64s = str(blob_base64)
    return blob_b64s


def make_url(blob_type:str, parameters:dict) -> str:
    if not blob_type in parameters.keys():
        parameters['blob_type'] = blob_type
    url = "/blob?"
    for key in parameters:
        url += f'{key}={parameters[key]}&'
    url = url[0:-1] 
    return url




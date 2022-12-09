import pdb
import json
from typing import List
import os
import re 
from shutil import copyfile 
from hashlib import sha256

from google.cloud import storage
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

def upload_blob_googlecloud(source_file_name: str, path: str):
    with open('config/config.yaml','r') as f:
        config_data = yaml.safe_load(f) 
    project_id = config_data['google_cloud']['project_id']
    strip_split_path = path.replace('gs://',"").split('/')
    bucket_name = strip_split_path.pop(0)
    destination_blob_name = "/".join(strip_split_path)
    storage_client = storage.Client(project=project_id)
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return True 

def save_blob(file_path: str, paths: list) -> bool:
    try:
        # save file to cabinet locations
        for path in paths:
            # if google cloud location:
            if re.search("^gs://",path):
                upload_blob_googlecloud(file_path, path)
            else: 
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


def make_url(endpoint:str, blob_type:str, parameters:dict) -> str:
    if not blob_type in parameters.keys():
        parameters['blob_type'] = blob_type
    url = endpoint+"?"
    for key in parameters:
        url += f'{key}={parameters[key]}&'
    url = url[0:-1] 
    return url






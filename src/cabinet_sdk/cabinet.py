import json
import pdb
import requests
import os

import cabinet_sdk.fns as f

ENV = os.getenv('ENV')
ROOT_URL = f.get_root_url(ENV)

def welcome(name):
    """Simple fn to test library is working"""
    return print(f'Welcome {name} to Cabinet')

def upload(metadata:dict, file_path:str) -> dict:
    """
    Add a new entry to the Cabinet System. Entry includes a blob in base64_str form and a dict of associated metadata
    """
    # NOTE: may need to move inside a nother fn so post and post_args aren't accessible to user
    blob = f.encode_blob(file_path)
    data = {'metadata':metadata, 'blob_b64s': blob}
    api_resp = requests.post(ROOT_URL+'/blob', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

def search(blob_type:str, parameters:dict) ->dict:
    """
    Returns metadata for all entries matching submitted search parameters
    """
    url = f.make_url(blob_type, parameters)
    api_resp = requests.get(ROOT_URL+url).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']
      

def update(blob_type:str, entry_id:int, update_data:dict):
    """
    Creates a soft update of the metadata associated with a stored blob
    """
    data = {'blob_type':blob_type, 'entry_id':entry_id, 'update_data':update_data}
    api_resp = requests.post(ROOT_URL+'/blob/update', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

# OTHER 

def feilds(blob_type:str)-> dict: 
    """
    Returns a dict where keys are the metadata fields for specified blob_type. Values are None.  
    """
    api_resp = requests.get(ROOT_URL+f'/blob/feilds?blob_type={blob_type}').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    fields:list = api_resp['body']['fields']
    fields_dict = dict.fromkeys(fields)
    return fields_dict


def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    pass 


def retrieve(blob_type: str, entry_id: int) -> bytes:
    """Returns blob in bytes"""
    api_resp = requests.get(ROOT_URL+f'/blob/retrieve?blob_type={blob_type}&entry_id={entry_id}')
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    blob_b64s = api_resp['body']['blob']
    blob_bytes = f.bytify(blob_b64s)
    return blob_bytes 
    




import json
import pdb
import requests
import os

import cabinet_sdk.fns as f

ROOT_URL = f.get_root_url( )
 
def welcome(name):
    """Simple fn to test library is working"""
    return print(f'Welcome {name} to Cabinet')

def upload(metadata:dict, file_path:str) -> dict:
    """
    Add a new entry to the Cabinet System. Provide as arguments the metadata and file path to your blob. Entry includes a blob in base64_str form and a dict of associated metadata. RETURNS: entry_id
    """
    # NOTE: may need to move inside a nother fn so post and post_args aren't accessible to user
    blob = f.encode_blob(file_path)
    data = {'metadata':metadata, 'blob_b64s': blob}
    api_resp = requests.post(ROOT_URL+'/blob', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

def search(blob_type:str, metadata_search_parameters:dict={}) ->dict:
    """
    Search Cabinet for entries within your specified blob_type that have metadata matching submitted metadata_search_parameters. RETURNS metadata for all entries matching submitted search parameters. If no search parameters are entered, all entries in this blob_type will be returned.
    """
    url = f.make_url(blob_type, metadata_search_parameters)
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

def fields(blob_type:str)-> dict: 
    """
    Returns a dict where keys are the metadata fields for specified blob_type. Values are None.  
    """
    api_resp = requests.get(ROOT_URL+f'/fields?blob_type={blob_type}').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    fields:list = api_resp['body'][blob_type]
    fields_dict = dict.fromkeys(fields)
    return fields_dict


def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    api_resp = requests.get(ROOT_URL+'/fields?blob_type=return_all_blob_types').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']


def retrieve(blob_type: str, entry_id: int) -> bytes:
    """Returns blob in bytes"""
    api_resp = requests.get(ROOT_URL+f'/blob/{blob_type}/{entry_id}')
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    blob_b64s = api_resp['body']['blob']
    blob_bytes = f.bytify(blob_b64s)
    return blob_bytes 
    




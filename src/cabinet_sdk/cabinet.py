import json
import pdb
import requests
import os

import cabinet_sdk.fns as f

ROOT_URL = f.get_root_url( )
 
def welcome(name):
    """Simple fn to test library is working"""
    return print(f'Welcome {name} to Cabinet')


def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    api_resp = requests.get(ROOT_URL+'/fields?blob_type=return_all_blob_types').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']


def fields(blob_type:str)-> list: 
    """
    Returns a list of metadata fields for specified blob_type  
    """
    api_resp = requests.get(ROOT_URL+f'/fields?blob_type={blob_type}').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body'][blob_type]
    

def upload(metadata:dict, file_path:str) -> dict:
    """
    Add a new entry to the Cabinet System. Provide as arguments the metadata and file path to your blob. Do not include blob_hash in metadata, it will be calculated automatically. RETURNS: entry_id
    """
    # NOTE: may need to move inside a nother fn so post and post_args aren't accessible to user
    blob_hash = f.encode_blob(file_path)
    metadata['blob_hash'] = blob_hash 
    data = {'metadata':metadata}
    api_resp = requests.post(ROOT_URL+'/blob', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    entry_id = api_resp['body']['entry_id']
    f.save_blob(file_path, api_resp['body']['paths']) 
    # update save status in cabinet db
    api_resp = requests.put(ROOT_URL+'/blob', json={'paths':api_resp['body']['paths']}).json()
    if api_resp != 200:
        raise Exception(api_resp['error_message'])
    return entry_id 
    

def search(blob_type:str, metadata_search_parameters:dict={}) ->dict:
    """
    Search Cabinet for entries within your specified blob_type that have metadata matching submitted metadata_search_parameters. RETURNS metadata for all entries matching submitted search parameters. If no search parameters are entered, all entries in this blob_type will be returned.
    """
    url = f.make_url(blob_type, metadata_search_parameters)
    api_resp = requests.get(ROOT_URL+url).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']
      

def update(blob_type:str, entry_id:int, update_data:dict) -> dict:
    """
    Creates a soft update of the metadata associated with a stored blob
    """
    data = {'blob_type':blob_type, 'current_entry_id':entry_id, 'update_data':update_data}
    api_resp = requests.post(ROOT_URL+'/blob/update', json=data).json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']

# OTHER 

def retrieve(blob_type: str, entry_id: int) -> list:
    """Returns url/file_paths to where blob is saved"""
    api_resp = requests.get(ROOT_URL+f'/blob/{blob_type}/{entry_id}').json()
    if api_resp['status_code'] != 200:
        raise Exception(api_resp['error_message'])
    return api_resp['body']['paths']
    
    




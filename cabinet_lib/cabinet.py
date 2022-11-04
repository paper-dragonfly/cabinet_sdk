import json
import pdb
import base64

from cabinet_lib.constants import ROOT_URL
import cabinet_lib.fns as f
from cabinet_lib.fns import flask_client_get as cget, flask_client_post as cpost, flask_requests_get as rget, flask_requests_post as rpost

def upload(metadata:dict, blob:str, post=rpost, post_args:dict={}) -> int:
    """
    Add a new entry to the Cabinet System. Entry includes a blob in base64_str form and a dict of associated metadata
    """
    # NOTE: may need to move inside a nother fn so post and post_args aren't accessible to user
    data = {'metadata':metadata, 'blob_b64s': blob}
    new_entry_id = post(ROOT_URL+'/blob', data, **post_args)
    return new_entry_id 

def search(blob_type:str, parameters:dict, get=rget, get_args={}):
    """
    Returns metadata for all entries matching submitted search parameters
    """
    url = f.make_url(blob_type, parameters)
    matches = get(ROOT_URL+url,**get_args)
    return matches  

def update(blob_type:str, entry_id:int, update_data:dict, post=rpost, post_args={}):
    """
    Creates a soft update of the metadata associated with a stored blob
    """
    data = {'blob_type':blob_type, 'entry_id':entry_id, 'update_data':update_data}
    update_entry_id = post(ROOT_URL+'/blob/update', data, **post_args)
    return update_entry_id 

# OTHER 

def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    pass 

def encode_blob(blob, blob_format:str = 'string'):
    """
    converts blob to base64 encoded string
    """
    blob_bytes = blob.encode('utf-8')
    blob_base64 = base64.b64encode(blob_bytes)
    blob_b64s = str(blob_base64)
    return blob_b64s

def feilds(blob_type:str, get=rget, get_args={})-> dict: 
    """
    Returns a dict where keys are the metadata fields for specified blob_type. Values are default 
    """
    fields:list = get(ROOT_URL+f'/blob/feilds?blob_type={blob_type}')
    fields_dict = dict.fromkeys(fields)
    return fields_dict




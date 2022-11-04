import json
import pdb
import requests

import psycopg2
import yaml

from cabinet_lib.constants import ROOT_URL


# FLASK get+post for requests/client
def flask_requests_get(url:str)->dict:
    return requests.get(url).json()


def flask_requests_post(url:str,data:dict,)->dict:
    return requests.post(url, json=data).json()


def flask_client_get(url:str,client)->dict:
    response = client.get(url)
    return json.loads(response.data.decode("ASCII"))


def flask_client_post(url:str, data:dict,client)->dict:
    response = client.post(url, data=json.dumps(data), content_type='application/json')
    return json.loads(response.data.decode("ASCII"))

    ###

def make_url(blob_type:str, parameters:dict) -> str:
    if not blob_type in parameters.keys():
        parameters['blob_type'] = blob_type
    url = "/blob?"
    for key in parameters:
        url += f'{key}={parameters[key]}&'
    url = url[0:-1] 
    return url
    ###

# def add_blob(blob_bytes:str):
#     data = {'blob_bytes':blob_bytes}
#     api_resp = requests.post(ROOT_URL+'/blob', json=data).json() 
#     blob_id = api_resp['blob_id']
#     return blob_id 

# def add_metadata(table, blob_id, metadata, new_blob=False) -> int:
#     metadata['blob_id'] = blob_id 
#     data = {'metadata':metadata, 'new_blob':new_blob}
#     api_resp = requests.post(ROOT_URL+f'{table}', json=data).json()
#     return api_resp['entry_id']
     

    
# def add(metadata:dict):
#     """add new entry to cabinet db. Use metadata to fill table. If key doesn't exist, add column to db"""



import requests
import os

import cabinet_sdk.fns as f

ROOT_URL = f.get_root_url()


def welcome(name):
    """Simple fn to test library is working"""
    return print(f"Welcome {name} to Cabinet")


def blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    api_resp = requests.get(ROOT_URL + "/fields?blob_type=return_all_blob_types").json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]


def schema(blob_type: str) -> list:
    """
    Returns a list of metadata schema for specified blob_type
    """
    api_resp = requests.get(ROOT_URL + f"/fields?blob_type={blob_type}").json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"][blob_type]


def get_store_envs(blob_type: str):
    """Returns possible hosts where blob can be stored"""
    return requests.get(ROOT_URL + f"/store_envs?blob_type={blob_type}").json()["body"][
        "envs"
    ]


def upload(metadata: dict, file_path: str, storage_environments: list) -> dict:
    """
    Add a new entry to the Cabinet System. Provide as arguments the blob metadata and file path as well as the environments you want the blob to be saved into (e.g. 'testing' or 'production'). Do not include blob_hash in metadata, it will be calculated automatically. RETURNS: entry_id
    """
    # NOTE: may need to move inside another fn so post and post_args aren't accessible to user
    # generate paths and save blob
    blob_hash = f.encode_blob(file_path)
    metadata["blob_hash"] = blob_hash
    blob_info = {"metadata": metadata, "storage_envs": storage_environments}
    api_resp = requests.post(ROOT_URL + "/storage_urls", json=blob_info).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    paths = api_resp["body"]["paths"]
    failed_saves = f.save_blob(file_path, paths)
    if failed_saves:
        paths = paths.difference(failed_saves)  # only successful saves
    # save metadata + save_paths to cabinet db
    api_resp = requests.post(
        ROOT_URL + "/blob",
        json={"metadata": metadata, "paths": paths, "new": api_resp["body"]["new"]},
    ).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    entry_id = api_resp["body"]["entry_id"]
    return {"entry_id": entry_id, "failed_saves": failed_saves}


def search(blob_type: str, metadata_search_parameters: dict = {}) -> dict:
    """
    Search Cabinet for entries within your specified blob_type that have metadata matching submitted metadata_search_parameters. RETURNS metadata for all entries matching submitted search parameters. If no search parameters are entered, all entries in this blob_type will be returned.
    """
    url = f.make_url("/blob/", blob_type, metadata_search_parameters)
    api_resp = requests.get(ROOT_URL + url).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]


def update(blob_type: str, entry_id: int, update_data: dict) -> dict:
    """
    Creates a soft update of the metadata associated with a stored blob
    """
    data = {
        "blob_type": blob_type,
        "current_entry_id": entry_id,
        "update_data": update_data,
    }
    api_resp = requests.post(ROOT_URL + "/blob/update", json=data).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]


def retrieve(blob_type: str, entry_id: int) -> list:
    """Returns url/file_paths to where blob is saved"""
    api_resp = requests.get(ROOT_URL + f"/blob/{blob_type}/{entry_id}").json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]["paths"]

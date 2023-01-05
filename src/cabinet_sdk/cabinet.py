import requests
import os

import cabinet_sdk.fns as f

ROOT_URL = f.get_root_url()


def check_health():
    """Simple fn to test library is working"""
    api_resp = requests.get(ROOT_URL + "/health").json()
    return print("SDK live\n", api_resp)


def list_blob_types():
    """
    Lists all blob_types stored in Cabinet and their metadata fields
    """
    api_resp = requests.get(ROOT_URL + "/fields?blob_type=return_all_blob_types").json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]


def list_schema(blob_type: str) -> list:
    """
    Returns a list of metadata schema for specified blob_type
    """
    api_resp = requests.get(ROOT_URL + f"/fields?blob_type={blob_type}").json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"][blob_type]


def get_storage_options(blob_type: str):
    """Returns possible hosts where blob can be stored"""
    return requests.get(ROOT_URL + f"/store_envs?blob_type={blob_type}").json()["body"][
        "envs"
    ]


def upload(metadata: dict, src: str, storage_environments: list) -> dict:
    """
    Add a new entry to the Cabinet System.
    Provide the blob metadata, file source and environments you want the blob to be saved into (e.g. 'testing' or 'production').
    Do not include blob_hash in metadata, it will be generated automatically.
    RETURNS: entry_id
    """
    # generate paths and save blob
    blob_hash = f.generate_blob_hash(src)
    metadata["blob_hash"] = blob_hash
    blob_info = {"metadata": metadata, "storage_envs": storage_environments}
    api_resp = requests.post(ROOT_URL + "/storage_urls", json=blob_info).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    paths = api_resp["body"]["paths"]
    failed_saves = f.save_blob(src, paths)
    if failed_saves:
        paths = list(set(paths).difference(failed_saves))  # only successful saves
    else:  # all saves successful
        failed_saves = None
    if not paths:  # blob did not successfully save anywhere
        return {"entry_id": None, "failed_saves": failed_saves}
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
    RETURNS metadata for all entries in Cabinet matching submitted search parameters.
    If no search parameters are entered, all entries in this blob_type will be returned.
    If no matches returns empty dict
    """
    url = f.make_url("/blob/", blob_type, metadata_search_parameters)
    api_resp = requests.get(ROOT_URL + url).json()
    if api_resp["status_code"] != 200:
        raise Exception(api_resp["error_message"])
    return api_resp["body"]


def update(blob_type: str, entry_id: int, update_data: dict) -> dict:
    """
    Creates a soft update of the metadata associated with an existing blob
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

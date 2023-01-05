# cabinet_sdk
Python library that allows users to access the Cabinet blob-storage system 

## Description 
Cabinet is a flexible blob-storage system that stores blobs and their associated metadata. It allows users to easily save and search for blobs based on their metadata values rather than file paths. The cabinet_sdk communicates with the cabinet_API which in turn interacts with the Cabinet postgreSQL database. 

Within Cabinet, entries are organized by blob_type. Each blob_type has its own metadata schema. For example your Cabinet might have a 'cat_thumbnails' blob_type with metadata fields [entry_id, blob_type, blob_hash, cat_color, cat_breed, photo_size, photographer'] 


## Installation 

Install using ```pip install -i https://test.pypi.org/simple/ cabinet-sdk``` 

must be used in conjunction with Cabinet-API. Download the Cabinet-API source code from github: '''https://github.com/paper-dragonfly/cabinet_api'''

must create config file (see configuration instructions below)

## What you can do - functions in cabinet_sdk
* check_health(): Simple fn to test library and API are working
* list_blob_types(): Get a list of all blob_types in your Cabinet 
* lis_schema(blob_type): Return a list of metadata fields for specified blob_type
* get_storage_options(blob_type): Returns possible hosts where blob can be stored
* upload(metadata, src, storage_environments): Add a blob and its associated metadata to Cabinet 
* search(blob_type, metadata_search_parameters): return metadata entries of specified blob_type that match metadata search parameters 
* update(blob_type, entry_id, update_dict): Creates a soft update of the metadata associated with an existing blob 
    * entry_id is a metadata field for all blob types. In this function, entry_id refers to an existing metadata entry associated with the blob of interest that you wish to update
* retrieve(blob_type, entry_id): Returns url/file_paths to where blob is saved. 

## Limitations 
Cabinet protects the information stored within it by limiting what users can do with the cabinet-sdk library. 

The user cannot: 
* add or delete blob_types
* alter blob_type metadata schema 
* alter existing metadata entries 
    * soft updates that create a new entry linked to an existing blob are permitted but old entries are not deleted or overwritten 
* alter blob content
* delete blobs 
* delete metadata entries

Creating, editing or deleting blob_types and their associated metadata schema must be done from the backend not the client 

## Configuration and setup
In order for cabinet-sdk to communicate with the cabinet-api you must provide the client with the API url. Add config/config.yaml to your root directory. If it already exists, simply add the cabinet specific code to the config.yaml file. In this file list your environments as keys and the root url on which the API is running as values. 

#### Sample contents of config.yaml 
---
cabinet:
    example_env: http://{host}:{port} 
    dev_local: http://localhost:5050
    testing: http://localhost:5050
    production: https://cabinet-api.onrender.com
    






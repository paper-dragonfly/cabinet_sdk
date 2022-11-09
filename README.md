# cabinet_sdk
Python library that allows users to access the Cabinet blob-storage system 

## Description 
Cabinet is a flexible blob-stroge system that stores blobs and thier associated metadata. It allows users to easily save and search for blobs based on their metadata values rather than relying on file paths as is the norm in conventional file systems. The cabinet_sdk communicates with the cabinet_API which in turn interacts with the Cabinet postgreSQL database. 

Within Cabinet entries are organized by blob_types. Each blob_type has it's own metadata schema. For example your Cabinet could have a 'cat_thumbnails' blob_type with metadata fields [entry_id, blob_type, cat_color, cat_breed, photo_size, photo_source'] or a 'student_essays' blob_type with metadata fields [entry_id, blob_type, student_name, student_DOB, subject, grade]


## Installation 

Install using ```pip install -i https://test.pypi.org/simple/ cabinet-sdk``` 

must be used in conjunction with cabinet-API (make link)
must create config file (see configuration below)

## What you can do - functions in cabinet_sdk
* welcome(): a simple function that confirms the library is working
* blob_type(): Get a list of all blob_types in your Cabinet 
* fields(blob_type): Get a dictionary containing as keys the metadata fields for the specified blob_type
* upload(metadata, blob): Add a blob and its associated metadata to Cabinet 
* search(blob_type, search_parameters): search for all metadata entries of specified blob_type that match the search parameters 
* update(): Creates a soft update of the metadata associated with a stored blob
* retrieve(blob_type, entry_id): returns blob in bytes 

## Limitations 
Cabinet protects the information stored within it by limiting what users can do with the cabinet-sdk library. 

The user cannot: 
* add or delete blob_types
* alter blob_type metadata schema 
* alter existing metadata entries - soft updates that create a new entry linked to an existing blob are permitted but old entries are not deleted or overwritten 
* alter blob content
* delete blobs 
* delete metadata entries

Creating, editing or deleting blob_types and their associated metadata schema must be done from the backend not the client 

## Configuration and setup
In order for cabinet-sdk to communicate with the cabinet-api you must provide the client with the API url. Add config/config.yaml to your root directory. If it already exists, simply add the cabinet specific code to the config.yaml file. In this file list your environments as keys and the root url on which the API is running as values. 

Sample contents of config.yaml 
---
cabinet:
    example_env: http://{host}:{port} 
    dev_local: http://localhost:5050
    testing: http://localhost:5050
    production: https://cabinet-api.horoku.com
    
Cabinet uses the environment variable ENV to determin which version of the cabinet database to connect to. The defualt is dev_local. However, there is also a test database that should be used when running the automated tests and in certain cases there may be more. To set the environment, enter the following into the terminal ```export ENV='{environment}'.





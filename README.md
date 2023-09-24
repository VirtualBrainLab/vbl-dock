# vbl-dock

Storage server for VBL JSON files

This is a Flask application that implements a REST API allowing for PUT/POST/GET access to JSON files stored on the server. The JSON files are not encrypted, but are protected by a password. This isn't really a secure setup, but whatever.

## Development

Run in dev mode by using `python server.py`, which loads the Flask server on `localhost:5000`

## Flask app

Users create a new bucket using the POST `/create/<bucket>` endpoint, passing a token and password:

```
data = {
    "token": "<token>",
    "password": hash256("<password>")
}
```

Users add new data to a bucket using the POST or PUT `/upload/<bucket>/<type>/<name>?auth=<hashed password>` endpoint, passing the data:

```
data = {
    "data": {
        "position": [1,2,3]
    }
}
```

Users access data in a bucket using GET `/<bucket>/<type>/<name>?auth=<hashed password>` which will return the raw JSON. 

## Folder structure

`/data/` is the top level folder.

Buckets are stored in `/data/bucket/`. Users then organize their data files by type (e.g. neurons, probes, etc) and with a unique name. P

## Hosting

todo...
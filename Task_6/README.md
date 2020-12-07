# Omdena X ISS Proof of Concept

## Quick Case Reference Powered by AI

### Usage

### For Developers

This app uses python version 3.8.

Create and activate virtual environment in this (Task_6) directory:
```
$ python3 -m venv env
$ source env/bin/activate
(env)$ pip install requirements.txt
```
If "ERROR: Could not find a version that satisfies the requirement requirements.txt (from versions: none)":
```
(env)$ pip install -r requirements.txt
```
When using conda evironment:
```
$ conda create --name omdena-iss python=3.8
$ conda activate omdena-iss
```

To run the app locally:
```
$ flask run
```
To enable debugging mode while running the app locally:
```
$ python3 app.py
```
#### Database
You'll need PostgreSQL >= 11.6.

To create a local database:
```
$ createdb iss
```
To update the model:
```
$ flask db migrate
$ flask db upgrade
```
To seed the model:
```
$ python3 seed.py seed
```

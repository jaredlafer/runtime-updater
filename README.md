# runtime-updater

This app is a proof of concept for an api running on a [flask](https://flask.palletsprojects.com/en/1.1.x/) server that is capable of updating its own functions runtime. It achieves this through [bytecode](https://en.wikipedia.org/wiki/Bytecode) injection. The client serializes a function represented as a [CodeObject](https://docs.python.org/3.8/c-api/code.html), and replaces a target function's CodeObject on the server. This app is a simple model, and not designed with a particular use case in mind, though here are some examples:
1. You need a server that once deployed would never be shut down, yet whose code needs to be capable of being updated.
2. You'd like profile runnning code.
3. You don't have the source code for a running application (e.g. only *.pyc files), and can only update at the level of bytecode.
4. You're working with a module that is obfuscated and difficult to modify in an automated way.



## Installation
Clone the repository

    $ git clone https://github.com/jaredlafer/runtime-updater.git
    $ cd runtime-updater
    $ mkdir logs

It is recommended you run this code in a [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/index.html).

Install dependencies using [pip](https://pip.pypa.io/en/stable/quickstart/):

    $ pip install -r requirements.txt
    
This code was tested on macOS Mojave Version 10.4.6, with python 3.8.6.

## Run The App

To run the server:

    $ python run.py
    
By default the app will run on `http://127.0.0.1:5000`

The app is created in `updateable_api/__init__.py`. The structure follows the standard [flask factory pattern](https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/). 
    
## Tests
Unit tests are written in tests.py, and can be run:
    
    $ python -m unittest tests
    
The tests here provide examples of how a developer might prepare functions to update another function on the server.

## Functionality
As this is a proof of concept, the only route in `updateable_api/views.py` that can be updated is 
```python
@update_bp.route('/', methods=['GET'])
def foobar_endpoint():
    ...
```
This calls a function 
```python
def foobar():
    ...
```
in `updateable_api/updateable_functions.py` that can be updated. This function is intentionally empty for demonstration purposes. With `foobar_endpoint()` fixed, any function (e.g. `foobar()`) that `foobar_endpoint()` calls could be updated runtime with
```python
@update_bp.route('/update_endpoint', methods=["POST"])
def update():
    ...
```
as long as the updated function returns objects that are json serializable. It is assumed that the developer has thoroughly tested the function contained in the `update()` payload and can ensure its compatibility with the application. If a buggy or incompatible function is injected a 500 status will be returned when the endpoint is called.

## Logging
Logging supports three modes "stream," "watched," and "rotate," with handlers for both a default and an access log. The logs are set up in `updateable_api_logs.py`. Log environment variables are stored in `settings.py`. Every request is logged. The logging is compatible with the flask factory pattern. Logging code was adapted from: https://github.com/tenable/flask-logging-demo.

## Limitations
The code does not support updating flask routes or classes. For routes, I didn't have the time to untangle the flask code from the bytecode, so made a design choice to require that only functions that aren't routes could be updated. Likewise, I didn't have the time to implement injection for classes, though anticipate this being more complex than functions.

A WatchedHandler cannot be used for logging on Windows because on Windows open log files cannot be moved or renamed (see https://docs.python.org/3/library/logging.handlers.html)

## TODO
Fix all the limitations above.  
Implement a system for version control (e.g. github for bytecode injection).  
Write tests for logging.  
Write proper integration tests.  
Test on other operating systems.  

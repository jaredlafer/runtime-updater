# runtime-updater

This app is a proof of concept for an api running on a flask server that is capable of updating its own functions runtime. It achieves this through bytecode injection. The client serializes a function represented as a [CodeObject](https://docs.python.org/3.8/c-api/code.html), and replaces a specified function's CodeObject on the server. This code is simplified and not designed with a particular use case in mind, though if you had to design a server that could never be shutdown, this shows how bytecode injection could achieve live versioning functionality.

## Installation
Clone the repository

    $ git clone https://github.com/jaredlafer/runtime-updater.git

It is recommended you run this code in a [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/index.html).

Install dependencies using [pip](https://pip.pypa.io/en/stable/quickstart/):

    $ pip install -r requirements.txt
    
This code was tested on macOS Mojave Version 10.4.6, with python 3.8.6.

## Run The App

To run the server:

    $ python run.py
    
By default the app will run on `http://127.0.0.1:5000`
    
## Tests
Unit tests are written in tests.py, and can be run:
    
    $ python -m unittest tests
    
The tests here provide an examples of how the client might prepare functions to update another function on the server.

## Functionality
The structure follows the standard flask factory pattern. As this is a proof of concept, the only route in `updateable_api/views` that can be updated is 
```python
def foobar_endpoint()
```
This calls a function 
```python
def foobar()
```
in `updateable_api/updateable_functions.py` that can be updated. With foobar_endpoint fixed, any function (e.g. `foobar()`) that foobar_endpoint calls could be updated runtime with
```python
def update()
```
as long as the updated function returns objects that are json serializable. It is assumed that the user has thoroughly tested the function contained in the `update()` payload and can ensure its compatibility with the application. If a buggy or incompatible function is injected the application will break.

## Logging
Logging supports three modes "stream," "watched," and "rotate," with handlers for both a default and an access log. Log environment variables are stored in `settings.py` The logging is compatible with the flask factory pattern. Logging code was adapted from: https://github.com/tenable/flask-logging-demo

## Limitations
The code does not support updating flask routes or classes. For routes, I didn't have the time to untangle the flask code from the bytecode, so made a design choice to require that only functions that routes call could be updated. I didn't have the time to implement injection for classes.

A WatchedHandler cannot be used for logging on Windows because on Windows open log files cannot be moved renamed (see https://docs.python.org/3/library/logging.handlers.html)

## TODO
Fix all the limitations above.
Implement a system for version control (e.g. github for bytecode injection)
Write tests for logging
Test on other operating systems

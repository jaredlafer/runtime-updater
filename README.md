# runtime-updater

This app is a proof of concept for an api running on a flask server that is capable of updating its own functions runtime. It achieves this through bytecode injection. The client serializes a function represented as a CodeObject [https://docs.python.org/3.8/c-api/code.html], and replaces a specified function's CodeObject on the server. This code is simplified and not designed with a particular use case in mind, though if you had to design a server that could never be shutdown, this shows how bytecode injection could achieve live versioning functionality.

## Installation



To run the server:

    $ python run.py

## Dependencies
Install dependencies using [pip] (https://pip.pypa.io/en/stable/quickstart/):

    $ pip install -r requirements.txt
    
This code was tested on macOS Mojave Version 10.4.6, with python 3.8.6.

## Structure
The structure follows the standard flask factory pattern. As this is a demonstration, the only route in `updateable_api/views` that can be updated is 
```python
def foobar_endpoint()
```
This calls a function 
```python
def foobar()
```
in `updateable_api/updateable_functions.py` that can be updated. With foobar_endpoint fixed, any function that foobar_endpoint calls could be updated runtime with
```python
def update()
```

## Logging
Logging supports three modes "stream," "watched," and "rotate," with both "access" and  . Environment variables are stored in `settings.py` The logging is compatible with the flask factory pattern.

## Tests
Unit tests are written in tests.py, and can be run:
    
    $ python -m unittest tests
    
This provides an example of how the client might update a function on the server.

## Limitations
The code does not support updating flask routes or classes. For routes, I didn't have the time to untangle the flask code from the bytecode, so made a design choice to require that only functions that routes call could be updated. I didn't have the time to implement classes.

A WatchedHandler cannot be used for logging on Windows because on Windows open log files cannot be moved renamed (see https://docs.python.org/3/library/logging.handlers.html)

## TODO
Fix all the limitations above.
Implement a system for version control (github for bytecode injection)
Write tests for logging
Test on other operating systems

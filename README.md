A 2p grid game.

# How to contribute

## Setting up the environment

### Install cofeescript locally

    npm install

### Install flask server as a module in a python environment

    source bin/activate
    python3 -m venv /path/to/new/virtual/environment
    pip install --editable .

## Normal development

### Compiling the coffeescript

    ./node_modules/coffeescript/bin/coffee -o grid/static/js/ -cw grid/coffee/

### Running the flask server:

    export FLASK_APP=grid
    export FLASK_DEBUG=1
    flask run



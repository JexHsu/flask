# Usage

Creates a Python virtual environment named .venv

`python3 -m venv .venv`

Activates the virtual environment

`source .venv/bin/activate`

Installs Flask package into the virtual environment

`pip install flask`

Initializes the database for the Flaskr application

`flask --app flaskr init-db`

Runs the Flaskr application in debug mode

`flask --app flaskr run --debug`


# Web Shell

Portable HTTP Server to run shell commands passed as HTTP requests

Very hacky; not for production usage

## Usage
To start the server, run the script as follows:

    WEB_SHELL_TOKEN=$(python3 -c 'import uuid; print(uuid.uuid4())')
    WEB_SHELL_PORT=4001
    ./web_shell.py

To invoke a command:

    COMMAND=/srv/www/
    curl "http://hostname.com:4001/?token=$WEB_SHELL_TOKEN&command=$COMMAND"

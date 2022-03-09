#!/usr/bin/python3

# https://linuxhint.com/use-python-simplehttpserver
import http.server
import os
import subprocess
import urllib
import sys

SCRIPT_NAME = os.path.basename(sys.argv[0])
prefix = SCRIPT_NAME.split('.py')[0].upper()

HOST = os.getenv(f"{prefix}_HOST", "0.0.0.0")
PORT = int(os.getenv(f"{prefix}_PORT", "4001"))
TOKEN = os.environ[f"{prefix}_TOKEN"]


def get_qs_params(url):
    return urllib.parse.parse_qs(urllib.parse.urlparse(url).query)


def run_command(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')
    return output


class PythonServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        querystring_params = get_qs_params(self.path)
        command = querystring_params.get('command', [''])
        command = next(iter(command))
        token = querystring_params.get('token', [''])
        token = next(iter(token))
        # token is required

        response_text = "OK"
        if command and token == TOKEN:
            token = querystring_params['token']
            print("running command: ", command)
            stdout = run_command(command)
            response_text = "\n".join((f"Running command: {command}", f"Command output: {stdout}"))

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(response_text.encode())

webServer = http.server.HTTPServer((HOST, PORT), PythonServer)

print("Server started http://%s:%s" % (HOST, PORT))

try:
    webServer.serve_forever()
except KeyboardInterrupt:
    webServer.server_close()
    print("The server is stopped.")

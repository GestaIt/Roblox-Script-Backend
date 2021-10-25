"""
  " webServer.py
  " Handles the addition of an HTTP server.
  " Gestalt 10/25/21
"""

from logging import getLogger, INFO

from flask import Flask, request
from flask_restful import Api, Resource
from ipwhois import IPWhois
from waitress import serve

from src.HTTPServer.requestParsers import scriptPostParser, scriptDeleteParser
from src.SQLServer import insert_script, remove_script, get_scripts, is_key_real

cached_ips = {"127.0.0.1": True}  # Our local ip.


# Checks if the given client ip address is from Roblox.
def check_ip(request_ip: str) -> bool:
    if request_ip in cached_ips:
        return cached_ips[request_ip]

    whois_information = IPWhois(request_ip).lookup_rdap()

    try:
        from_roblox = whois_information["objects"]["RC-376"]["contact"]["name"] == "Roblox"

        cached_ips[request_ip] = from_roblox
    except KeyError:
        return False

    return from_roblox


class ScriptsListGet(Resource):
    @staticmethod
    def get() -> tuple[list, int]:
        headers = request.headers
        client_ip = request.remote_addr
        is_from_roblox = check_ip(client_ip)

        if is_from_roblox:
            if "AUTH-TOKEN" in headers:
                auth_token = headers["AUTH-TOKEN"]

                if is_key_real(auth_token):
                    scripts_fetch_success, scripts = get_scripts(auth_token)

                    if scripts_fetch_success:
                        return scripts, 200

        return [], 500


class InsertScriptPost(Resource):
    @staticmethod
    def post() -> int:
        headers = request.headers
        client_ip = request.remote_addr
        is_from_roblox = check_ip(client_ip)

        if is_from_roblox:
            if "AUTH-TOKEN" in headers:
                auth_token = headers["AUTH-TOKEN"]

                if is_key_real(auth_token):
                    request_arguments = scriptPostParser.parse_args()
                    script_name = request_arguments["sName"]
                    script_description = request_arguments["sDescription"]
                    script_source = request_arguments["sSource"]

                    insert_success = insert_script(script_name, script_description, script_source, auth_token)

                    if insert_success:
                        return 200

        return 500


class RemoveScriptDelete(Resource):
    @staticmethod
    def delete() -> int:
        headers = request.headers
        client_ip = request.remote_addr
        is_from_roblox = check_ip(client_ip)

        if is_from_roblox:
            if "AUTH-TOKEN" in headers:
                auth_token = headers["AUTH-TOKEN"]

                if is_key_real(auth_token):
                    request_arguments = scriptDeleteParser.parse_args()
                    script_name = request_arguments["sName"]

                    delete_success = remove_script(script_name, auth_token)

                    if delete_success:
                        return 200

        return 500


# Runs the HTTP server on port 80.
def run_server():
    app = Flask(__name__)
    api = Api(app)

    logger = getLogger("waitress")
    logger.setLevel(INFO)

    api.add_resource(ScriptsListGet, "/api/v1/scripts/list")
    api.add_resource(InsertScriptPost, "/api/v1/scripts/insert")
    api.add_resource(RemoveScriptDelete, "/api/v1/scripts/remove")

    print("serving webserver")
    serve(app, host="0.0.0.0", port=80, threads=4, connection_limit=500)

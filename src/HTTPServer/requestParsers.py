"""
  " requestParsers.py
  " Stores the parse templates for cURL requests
  " Gestalt 10/25/21
"""

from flask_restful import reqparse

scriptPostParser = reqparse.RequestParser()
scriptPostParser.add_argument("sName", required=True, type=str, help="Script Name")
scriptPostParser.add_argument("sDescription", required=True, type=str, help="Script Description")
scriptPostParser.add_argument("sSource", required=True, type=str, help="Script Source")

scriptDeleteParser = reqparse.RequestParser()
scriptDeleteParser.add_argument("sName", required=True, type=str, help="Script Name")

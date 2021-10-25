"""
  " scriptManager.py
  " Handles script manipulation.
  " Gestalt 10/25/21
"""

import os
import sqlite3
from datetime import datetime

working_directory = os.getenv("working directory", os.getcwd())
scripts_database = f"{working_directory}/Scripts.db"

database_exists = os.path.exists(scripts_database)


def write_schema_to_db():
    with sqlite3.connect(scripts_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("""
                CREATE TABLE scripts(
                    affiliatedKey TEXT PRIMARY KEY,
                    scriptName TEXT,
                    scriptDescription TEXT,
                    scriptSource TEXT,
                    timeAdded INTEGER
                )""")
        except sqlite3.Error:
            print("Failed to load schema")

        connection.commit()
        cursor.close()


if not database_exists:
    write_schema_to_db()

"""
schema:

CREATE TABLE scripts(
    affiliatedKey TEXT PRIMARY KEY,
    scriptName TEXT,
    scriptDescription TEXT,
    scriptSource TEXT,
    timeAdded INTEGER
)
"""


# Inserts a new script into the SQL database. Returns whether the operation was a success or not.
def insert_script(script_name: str, script_description: str, script_source: str, api_key: str) -> bool:
    with sqlite3.connect(scripts_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO scripts VALUES (:aToken, :sName, :sDescription, :sSource, :dTime)",
                           {"aToken": api_key, "sName": script_name, "sDescription": script_description,
                            "sSource": script_source, "dTime": datetime.today().timestamp()})
        except sqlite3.Error as err:
            print(f"Failed to add {script_name} to database. The following error occurred:\n\n{err}")
            return False

        return True


# Removes an existing script from the SQL database. Returns whether the operation was a success or not.
def remove_script(script_name: str, api_key: str) -> bool:
    with sqlite3.connect(scripts_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM scripts WHERE :sName=scriptName AND :aToken=affiliatedKey",
                           {"sName": script_name, "aToken": api_key})
        except sqlite3.Error as err:
            print(f"Failed to remove {script_name} from database. The following error occurred:\n\n{err}")
            return False

        return True


# Gets all of the scripts from the SQL database. Returns whether the operation was a success or not
# and the script information inside of a dictionary.
def get_scripts(api_key: str) -> tuple[bool, list[str, int]]:
    with sqlite3.connect(scripts_database) as connection:
        cursor = connection.cursor()

        try:
            scripts = cursor.execute("SELECT * FROM scripts WHERE :aToken=affiliatedKey",
                                     {"aToken": api_key}).fetchall()
        except sqlite3.Error as err:
            print(f"Failed to get all of the scripts. The following error occurred:\n\n{err}")
            return False, []

        return True, scripts

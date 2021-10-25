"""
  " keyManager.py
  " Handles the creation of keys.
  " Gestalt 10/25/21
"""

import os
import sqlite3

working_directory = os.getenv("working directory", os.getcwd())
key_database = f"{working_directory}/Keys.db"

database_exists = os.path.exists(key_database)


def write_schema_to_db():
    with sqlite3.connect(key_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("""
                CREATE TABLE keys(
                    key TEXT PRIMARY KEY
                )""")
        except sqlite3.Error:
            print("Failed to load schema")

        connection.commit()
        cursor.close()


if not database_exists:
    write_schema_to_db()

"""
schema:

CREATE TABLE keys(
    key TEXT PRIMARY KEY
)
"""


# Inserts the new key into the key database.
def insert_key(new_key: str) -> bool:
    with sqlite3.connect(key_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("INSERT INTO keys VALUES (:nKey)",
                           {"nKey": new_key})
        except sqlite3.Error as err:
            print(f"Failed to insert a new key. The following error occurred:\n\n{err}")
            return False

        return True


# Checks if the specified key exists.
def is_key_real(api_key: str) -> bool:
    with sqlite3.connect(key_database) as connection:
        cursor = connection.cursor()

        try:
            exists = cursor.execute("SELECT * FROM keys WHERE :aKey=key",
                                    {"aKey": api_key}).fetchone()
        except sqlite3.Error:
            return False

        return bool(exists)


# Removes a key from the key database.
def remove_key(api_key: str) -> bool:
    with sqlite3.connect(key_database) as connection:
        cursor = connection.cursor()

        try:
            cursor.execute("DELETE FROM keys WHERE :aKey=key",
                           {"aKey": api_key})
        except sqlite3.Error as err:
            print(f"Failed to remove a key. The following error occurred:\n\n{err}")
            return False

        return True

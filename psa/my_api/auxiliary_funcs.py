import json
import os
import configparser

def is_import_json_valid(data):
    relatives = dict()
    for citizen in data['citizens']:
        if citizen['citizen_id'] in relatives:
            return False
        else:
            relatives[citizen['citizen_id']] = set(citizen['relatives'])
    for citizen in relatives:
        for relative in relatives[citizen]:
            if citizen not in relatives[relative]:
                return False
    return True

def create_import_conf():
    config = configparser.ConfigParser()
    config.add_section("Import")
    config.set("Import", "last_import_id", "0")
    with open("config.py", "w") as config_file:
        config.write(config_file)

def generate_import_id(set_zero=False):
    if set_zero==True or not os.path.exists("config.py"):
        create_import_conf()
    else:
        config = configparser.ConfigParser()
        config.read("config.py")
        config.set("Import", "last_import_id", str(get_import_id() + 1))
        with open("config.py", "w") as config_file:
            config.write(config_file)

def get_import_id():
    config = configparser.ConfigParser()
    config.read("config.py")
    import_id = int(config.get("Import", "last_import_id"))
    return import_id
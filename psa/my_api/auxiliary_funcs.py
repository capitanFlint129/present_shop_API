import json
import os
import configparser
import datetime

def is_relative_ties_valid(data):
    relatives = dict()
    try:
        for citizen in data['citizens']:
            if citizen['citizen_id'] in relatives:
                return False
            else:
                if citizen['relatives'] == None: return False
                relatives[citizen['citizen_id']] = set(citizen['relatives'])
    
        for citizen in relatives:
            for relative in relatives[citizen]:
                if citizen not in relatives[relative] or relative == citizen:
                    return False
    except KeyError:
        return False
    return True



def create_import_conf():
    config = configparser.ConfigParser()
    config.add_section("Import")
    config.set("Import", "last_import_id", "0")
    with open("import_config.py", "w") as config_file:
        config.write(config_file)

def generate_import_id():
    if not os.path.exists("import_config.py"):
        create_import_conf()
    else:
        config = configparser.ConfigParser()
        config.read("import_config.py")
        #if get_import_id == 9223372036854775807:
        config.set("Import", "last_import_id", str(get_import_id() + 1))
        with open("import_config.py", "w") as config_file:
            config.write(config_file)

def get_import_id():
    config = configparser.ConfigParser()
    config.read("import_config.py")
    import_id = int(config.get("Import", "last_import_id"))
    return import_id



def add_present(month, relative):
    for citizen in month:
        if citizen['citizen_id'] == relative:
            citizen['presents'] += 1
            return
    month.append({'citizen_id': relative, 'presents': 1})

def calculate_age(born):
    today = datetime.datetime.utcnow()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

def add_age(cities, city, birth_date):
    age = calculate_age(birth_date)
    if city in cities:
        cities[city].append(age)
    else:
        cities[city] = [age]
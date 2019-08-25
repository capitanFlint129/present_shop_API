import json
import os
import configparser
import datetime
from my_api.models import Citizen

def is_relative_ties_valid(data):
    relatives = dict()
    try:
        #if not data['citizens']:
        #    return False
        for citizen in data['citizens']:
            if citizen['citizen_id'] in relatives:
                return False
            else:
                if citizen['relatives'] == None: return False
                relatives[citizen['citizen_id']] = set()
                for relative in citizen['relatives']:
                    if relative in relatives[citizen['citizen_id']] or relative == citizen['citizen_id']:
                        return False
                    else:
                        relatives[citizen['citizen_id']].add(relative)
    
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
    import_id_list = sorted(list(set(i.import_id for i in Citizen.objects.all())))
    is_generated = False
    for i in range(len(import_id_list)):
        if i != import_id_list[i]:
            config.set("Import", "last_import_id", str(i))
            is_generated = True
    
    if not is_generated:
        config.set("Import", "last_import_id", str(len(import_id_list)))

    with open("import_config.py", "w") as config_file:
        config.write(config_file)

def generate_import_id():
    if not os.path.exists("import_config.py"):
        create_import_conf()
    else:
        config = configparser.ConfigParser()
        config.read("import_config.py")
        last_import_id = int(config.get("Import", "last_import_id"))
        import_id_set = set(i.import_id for i in Citizen.objects.all())
        while last_import_id in import_id_set:
            if last_import_id == 9223372036854775807:
                create_import_conf()
            last_import_id += 1

        config.set("Import", "last_import_id", str(last_import_id))
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

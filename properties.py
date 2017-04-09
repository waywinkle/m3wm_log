import os
import json


def get_all_properties(property_file='properties.json'):
    with open(get_file_location(property_file)) as json_file:
        properties = json.load(json_file)

    return properties


def get_property(json_property, property_file='properties.json'):
    properties = get_all_properties(property_file)
    return properties[json_property]


def get_file_location(file_name):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    return os.path.join(__location__, file_name)

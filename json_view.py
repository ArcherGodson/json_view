#!/usr/bin/env python3

import json
import sys
import re 
import datetime

issue = json.load(sys.stdin)


def get_color_by_value(value):
    color = 0
    if str(value).lower() in ["red", "off", "error", "disable"]: 
        color = "31"
    if str(value).lower() in ["green", "on", "true", "enable"]: 
        color = "32"
    if str(value).lower() in ["yellow", "ip"] or re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", str(value)): 
        color = "33"
    try:
        a=datetime.datetime.fromisoformat(str(value))
        color = "37;2"
    except:
        pass
    if str(value).lstrip("-").replace(".","",1).isnumeric(): 
        color = "36"
    return color


def print_key_value(indent, key='', value=''):
    key = key+": " if key != "" else ""
    value_color = get_color_by_value(value)
    print("{0}\033[1m{1}\033[{3}m{2}\033[0m".format(" " * indent, key, value, value_color))


def get_json_structure(item, indent):
    if type(item) is list:
        for item_l in item:
            get_json_structure(item_l, indent + 2)
    #            print()

    elif type(item) is dict:
        for item_d in item.keys():
            if type(item[item_d]) is list:
                print_key_value(indent, key=item_d)
                get_json_structure(item[item_d], indent)
            elif type(item[item_d]) is dict:
                print_key_value(indent, key=item_d)
                get_json_structure(item[item_d], indent + 2)
            else:
                print_key_value(indent, key=item_d, value=item[item_d])
    else:
        print_key_value(indent, value=item)


get_json_structure(issue, 0)

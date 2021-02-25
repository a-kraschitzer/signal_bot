from collections import namedtuple
import html
import json
import random


def get_random_element(array):
    return array[random.randrange(len(array))]


def sanitize(string_in):
    return html.unescape(string_in).replace('"', "'")


def json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=json_object_hook)


def none(check):
    return check is None


def n_none(check):
    return not none(check)



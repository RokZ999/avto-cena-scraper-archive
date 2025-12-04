from datetime import datetime


def remove_fields_from_single_json(json_data, fields):
    for field in fields:
        if field in json_data:
            del json_data[field]


def remove_fields_from_list_of_json(list_of_json_data, fields):
    for item in list_of_json_data:
        remove_fields_from_single_json(item, fields)


def add_datetime_to_single_json(json_data):
    json_data['date_of_insert'] = datetime.now()


def add_datetime_to_list_of_json(list_of_json_data):
    for item in list_of_json_data:
        if isinstance(item, dict):
            add_datetime_to_single_json(item)




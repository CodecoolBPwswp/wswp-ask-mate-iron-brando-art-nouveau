import datetime


def get_current_time():
    current_time_str = str(datetime.datetime.now())[:16]
    return current_time_str


def add_submission_time(dict_of_new_entry):
    dict_of_new_entry["submission_time"] = get_current_time()
    return dict_of_new_entry


def add_missing_fields(dict_to_check, header): # vote és view should be 0
    for field_name in header:
        if field_name not in dict_to_check:
            dict_to_check[field_name] = None
    return dict_to_check


def initialize_counter_fields(dict_of_entry, field_names):
    for field in field_names:
        dict_of_entry[field] = 0
    return dict_of_entry

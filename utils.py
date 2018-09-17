import datetime


def add_submission_time(dict_of_new_entry):
    current_time_str = str(datetime.datetime.now())[:16]
    dict_of_new_entry["submission_time"] = current_time_str
    return dict_of_new_entry


def add_missing_fields(dict_to_check, header): # vote és view should be 0
    for field_name in header:
        if field_name not in dict_to_check:
            dict_to_check[field_name] = None
    return dict_to_check

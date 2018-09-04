import datetime
import uuid


def add_id_to_entry(dict_of_new_entry):
    dict_of_new_entry["id"] = uuid.uuid4()
    return dict_of_new_entry


def add_submission_time(dict_of_new_entry):
    current_time_str = str(datetime.datetime.now())
    dict_of_new_entry["submission_time"] = current_time_str
    return dict_of_new_entry


def add_missing_fields(dict_to_check, header): # vote és view should be 0
    for field_name in header:
        if field_name not in dict_to_check:
            dict_to_check[field_name] = None
    return dict_to_check


def check_if_all_fields(dict_to_check, header):
    for field_name in header:
        if field_name not in dict_to_check:
            error_message = "Missing field from new line: {}".format(field_name)
            raise KeyError(error_message)


def get_line_by_id(dict_of_lines, _id, field_to_check="id", as_list=False):
    filtered_lines = [line for line in dict_of_lines if line[field_to_check] == _id]
    object_to_return = None
    if not as_list:
        object_to_return = filtered_lines[0]
    else:
        object_to_return = filtered_lines
    return object_to_return


def update_line_in_list_of_dicts(list_of_dicts, updated_dict):
    """
    Updates a line in the given list of dictionaries,
    :param list_of_dicts: The list in which we want to update an item
    :param updated_dict: A dictionary that should replace the old values
    :return: None
    """
    line_to_update = get_line_by_id(list_of_dicts, updated_dict["id"])
    index_to_update = list_of_dicts.index(line_to_update)
    list_of_dicts[index_to_update] = updated_dict
    return list_of_dicts


def increase_field_by_1(data, _id, field_name):
    line_to_update = get_line_by_id(data, _id)
    line_to_update[field_name] += 1
    updated_data = update_line_in_list_of_dicts(data, line_to_update)
    return updated_data


def decrease_field_by_1(data, _id, field_name):
    line_to_update = get_line_by_id(data, _id)
    line_to_update[field_name] -= 1
    updated_data = update_line_in_list_of_dicts(data, line_to_update)
    return updated_data


def set_integer_fields(data, list_of_field_names):
    for field in list_of_field_names:
        for line in data:
            line[field] = int(line[field])
    return data

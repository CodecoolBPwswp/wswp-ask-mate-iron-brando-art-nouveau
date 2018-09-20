import datetime
import bcrypt


def get_current_time():  # timestamp should be sliced when displayed not when stored!
    current_time_str = str(datetime.datetime.now())
    return current_time_str


def add_submission_time(dict_of_new_entry):
    dict_of_new_entry["submission_time"] = get_current_time()
    return dict_of_new_entry


def add_missing_fields(dict_to_check, header):
    for field_name in header:
        if field_name not in dict_to_check:
            dict_to_check[field_name] = None
    return dict_to_check


def initialize_counter_fields(dict_of_entry, field_names):
    for field in field_names:
        dict_of_entry[field] = 0
    return dict_of_entry


def create_password_hash(plain_text_password):
    hashed_password = bcrypt.hashpw(plain_text_password.encode("utf-8"), bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def verify_password(entered_password, hashed_password):
    is_correct = None
    try:
        is_correct = bcrypt.checkpw(entered_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except ValueError:
        is_correct = False
    return is_correct


def store_password_hash(dict_of_user):
    dict_of_user["password_hash"] = create_password_hash(dict_of_user["plain_text_password"])
    dict_of_user.pop("plain_text_password")
    return dict_of_user

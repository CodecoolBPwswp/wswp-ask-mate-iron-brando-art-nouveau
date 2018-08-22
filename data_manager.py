import connection
import datetime
import uuid

FILE_PATH_TO_QUESTIONS = "questions.csv"
FILE_PATH_TO_ANSWERS = "answers.csv"
HEADER_QUESTIONS = ["id", "submission_time", "view_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    list_of_questions = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_QUESTIONS)
    return list_of_questions


def add_new_question(dict_of_new_question):
    # expected fields: view_number, title, message, image
    dict_of_new_question = add_id_to_entry(dict_of_new_question)
    dict_of_new_question = add_submission_time(dict_of_new_question)
    for field_name in HEADER_QUESTIONS:
        if field_name not in dict_of_new_question:
            error_message = "Missing field from new question: {}".format(field_name)
            raise KeyError(error_message)
    connection.append_line_to_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, dict_of_new_question)


def add_id_to_entry(dict_of_new_entry):
    dict_of_new_entry["id"] = uuid.uuid4()
    return dict_of_new_entry


def add_submission_time(dict_of_new_entry):
    current_time_str = str(datetime.datetime.now())[:-7]
    dict_of_new_entry["submission_time"] = current_time_str
    return dict_of_new_entry


def get_line_by_id(dict_of_lines, _id, field_to_check="id"):
    filtered_line = [line for line in dict_of_lines if line[field_to_check] == _id][0]
    return filtered_line


def get_all_answers():
    list_of_answers = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_ANSWERS)
    return list_of_answers

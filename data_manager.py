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
    # fields to add: id, submission_time
    dict_of_new_question = add_id_to_entry(dict_of_new_question)
    dict_of_new_question = add_submission_time(dict_of_new_question)
    for field_name in HEADER_QUESTIONS:
        if field_name not in dict_of_new_question:
            raise KeyError("Missing field from new question: {field_name}")
    connection.append_line_to_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, dict_of_new_question)


def add_id_to_entry(dict_of_new_entry):
    dict_of_new_entry["id"] = uuid.uuid4()
    return dict_of_new_entry


def add_submission_time(dict_of_new_entry):
    current_time_str = str(datetime.datetime.now())[:-7]
    dict_of_new_entry["submission_time"] = current_time_str
    return dict_of_new_entry

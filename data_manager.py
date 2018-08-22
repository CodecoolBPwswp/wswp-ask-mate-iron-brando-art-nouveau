import connection
import utils

FILE_PATH_TO_QUESTIONS = "questions.csv"
FILE_PATH_TO_ANSWERS = "answers.csv"
HEADER_QUESTIONS = ["id", "submission_time", "view_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    list_of_questions = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_QUESTIONS)
    return list_of_questions


def add_new_question(dict_of_new_question):
    # expected fields: view_number, title, message, image
    dict_of_new_question = utils.add_id_to_entry(dict_of_new_question)
    dict_of_new_question = utils.add_submission_time(dict_of_new_question)
    check_if_all_fields(dict_of_new_question, HEADER_QUESTIONS)
    connection.append_line_to_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, dict_of_new_question)


def get_all_answers():
    list_of_answers = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_ANSWERS)
    return list_of_answers


def add_new_answer(dict_of_new_answer):
    # expected fields: vote_number, question_id, message, image
    dict_of_new_answer = utils.add_id_to_entry(dict_of_new_answer)
    dict_of_new_answer = utils.add_submission_time(dict_of_new_answer)
    check_if_all_fields(dict_of_new_answer, HEADER_ANSWERS)
    connection.append_line_to_csv(FILE_PATH_TO_ANSWERS, HEADER_ANSWERS, dict_of_new_answer)


def check_if_all_fields(dict_to_check, header):
    for field_name in header:
        if field_name not in dict_to_check:
            error_message = "Missing field from new line: {}".format(field_name)
            raise KeyError(error_message)


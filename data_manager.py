import connection
import utils

FILE_PATH_TO_QUESTIONS = "questions.csv"
FILE_PATH_TO_ANSWERS = "answers.csv"
HEADER_QUESTIONS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


def get_all_questions():
    list_of_questions = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_QUESTIONS)
    utils.set_integer_fields(list_of_questions, ["view_number", "vote_number"])
    return list_of_questions


def add_new_question(dict_of_new_question):
    # expected fields: view_number, title, message, image
    dict_of_new_question = utils.add_id_to_entry(dict_of_new_question)
    dict_of_new_question = utils.add_submission_time(dict_of_new_question)
    utils.check_if_all_fields(dict_of_new_question, HEADER_QUESTIONS)
    print(dict_of_new_question)
    connection.append_line_to_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, dict_of_new_question)


def get_all_answers():
    list_of_answers = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_ANSWERS)
    utils.set_integer_fields(list_of_answers, ["vote_number"])
    return list_of_answers


def add_new_answer(dict_of_new_answer):
    # expected fields: vote_number, question_id, message, image
    dict_of_new_answer = utils.add_id_to_entry(dict_of_new_answer)
    dict_of_new_answer = utils.add_submission_time(dict_of_new_answer)
    utils.check_if_all_fields(dict_of_new_answer, HEADER_ANSWERS)
    connection.append_line_to_csv(FILE_PATH_TO_ANSWERS, HEADER_ANSWERS, dict_of_new_answer)


def add_question_view(list_of_dicts, _id):
    updated_data = utils.increase_field_by_1(list_of_dicts, _id, "view_number")
    connection.update_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, updated_data)


def add_question_up_voting(list_of_dicts, _id):
    updated_data = utils.increase_field_by_1(list_of_dicts, _id, "vote_number")
    connection.update_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, updated_data)


def add_question_down_voting(list_of_dicts, _id):
    updated_data = utils.decrease_field_by_1(list_of_dicts, _id, "vote_number")
    connection.update_csv(FILE_PATH_TO_QUESTIONS, HEADER_QUESTIONS, updated_data)


def add_answer_up_voting(list_of_dicts, _id):
    updated_data = utils.increase_field_by_1(list_of_dicts, _id, "vote_number")
    connection.update_csv(FILE_PATH_TO_ANSWERS, HEADER_ANSWERS, updated_data)

def add_answer_down_voting(list_of_dicts, _id):
    updated_data = utils.decrease_field_by_1(list_of_dicts, _id, "vote_number")
    connection.update_csv(FILE_PATH_TO_ANSWERS, HEADER_ANSWERS, updated_data)


def add_answer_view(list_of_dicts, _id):
    updated_data = utils.increase_field_by_1(list_of_dicts, _id, "view_number")
    connection.update_csv(FILE_PATH_TO_ANSWERS, HEADER_ANSWERS, updated_data)

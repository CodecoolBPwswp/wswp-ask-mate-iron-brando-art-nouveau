import connection
import uuid

FILE_PATH_TO_QUESTIONS = "questions.csv"
FILE_PATH_TO_ANSWERS = "answers.csv"
HEADER_QUESTIONS = ["id", "submission_time", "view_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

def get_all_questions():
    list_of_questions = connection.read_csv_to_list_of_dicts(FILE_PATH_TO_QUESTIONS)
    return list_of_questions


def add_new_entry(entry_type, dict_of_new_entry):
    """
    Saves a new entry into the appropriate file
    :param entry_type: "question" or "answer"
    :param dict_of_new_entry: a dictionary that contains the values to save
    :return: None
    """
    pass


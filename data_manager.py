import csv
import uuid

FILE_PATH_TO_QUESTIONS = "questions.csv"
FILE_PATH_TO_ANSWERS = "answers.csv"
HEADER_QUESTIONS = ["id", "submission_time", "view_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]

def get_data_from_file(data_type):
    """
    Reads data from the chosen file
    :param data_type: "questions" or "answers"
    :return: list of dictionaries
    """
    file_data = get_file_data(data_type)
    with open(file_data["path"], "r", newline = "") as csvfile:
        reader = csv.reader(csvfile)
        data_lines = [row for row in reader][1:]
    list_of_dicts = []
    for line in data_lines:
        dict_of_line = dict(zip(file_data["header"], line))
        list_of_dicts.append(dict_of_line)
    return list_of_dicts


def add_new_entry(entry_type, dict_of_new_entry):
    """
    Saves a new entry into the appropriate file
    :param entry_type: "question" or "answer"
    :param dict_of_new_entry: a dictionary that contains the values to save
    :return: None
    """
    pass


def get_file_data(data_type):
    file_path = "default_path"
    data_header = ["default_header"]
    if data_type == "questions":
        file_path = FILE_PATH_TO_QUESTIONS
        data_header = HEADER_QUESTIONS
    elif data_type == "answers":
        file_path = FILE_PATH_TO_ANSWERS
        data_header = HEADER_ANSWERS
    else:
        raise ValueError("Invalid data type; choose from 'questions' or 'answers'")
    return {"path": file_path, "header": data_header}

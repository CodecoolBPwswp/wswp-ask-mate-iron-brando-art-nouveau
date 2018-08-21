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
    if data_type == "questions":
        file_path = FILE_PATH_TO_QUESTIONS
        header = HEADER_QUESTIONS
    elif data_type == "answers":
        file_path = FILE_PATH_TO_ANSWERS
        header = HEADER_ANSWERS

    with open(file_path, "r", newline = "") as csvfile:
        reader = csv.reader(csvfile)
        data_lines = [row for row in reader][1:]
    list_of_dicts = []
    for line in data_lines:
        dict_of_line = dict(zip(header, line))
        list_of_dicts.append(dict_of_line)
    return list_of_dicts



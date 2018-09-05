import connection
import utils

HEADER_QUESTIONS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT * FROM question
                    """)
    list_of_questions = cursor.fetchall()
    return list_of_questions


@connection.connection_handler
def get_question_by_id(cursor, _id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(id)s
                    """,
                   {'id': _id})
    dict_of_question = cursor.fetchone()
    return dict_of_question


@connection.connection_handler
def add_new_question(cursor, dict_of_new_question):  # to be refactored
    dict_of_new_question = utils.add_submission_time(dict_of_new_question)
    dict_of_new_question["view_number"] = 0
    dict_of_new_question["vote_number"] = 0
    dict_of_new_question["image"] = None
    dict_of_new_question = utils.add_missing_fields(dict_of_new_question, HEADER_QUESTIONS)
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image) 
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s)
                    """,
                   dict_of_new_question)


@connection.connection_handler
def get_all_answers(cursor):
    cursor.execute("""
                    SELECT * FROM answer
                    """)
    list_of_answers = cursor.fetchall()
    return list_of_answers


@connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %s;
                    """,
                   answer_id)
    dict_of_answer = cursor.fetchone()
    return dict_of_answer


@connection.connection_handler
def get_answers_by_question_id(cursor, _id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    """,
                   {'question_id': _id})
    answers_for_question = cursor.fetchall()
    return answers_for_question


@connection.connection_handler
def add_new_answer(cursor, dict_of_new_answer):  # to be refactored
    dict_of_new_answer = utils.add_submission_time(dict_of_new_answer)
    dict_of_new_answer["vote_number"] = 0
    dict_of_new_answer["image"] = None
    dict_of_new_answer = utils.add_missing_fields(dict_of_new_answer, HEADER_ANSWERS)
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                    """,
                   dict_of_new_answer)


@connection.connection_handler
def update_answer(cursor, dict_of_updated_answer):
    cursor.execute("""
                    UPDATE answer
                    SET message = %(message)s
                    WHERE id = %(answer_id)s;
                    """,
                   {"message": dict_of_updated_answer["message"],
                    "answer_id": dict_of_updated_answer["id"]})


@connection.connection_handler
def add_question_view(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


@connection.connection_handler
def add_answer_upvote(cursor, _id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


@connection.connection_handler
def add_answer_downvote(cursor, _id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


@connection.connection_handler
def add_question_upvote(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


@connection.connection_handler
def add_question_downvote(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})

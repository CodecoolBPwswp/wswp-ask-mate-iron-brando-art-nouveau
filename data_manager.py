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
def add_new_question(cursor, dict_of_new_question):
    dict_of_new_question = utils.add_submission_time(dict_of_new_question)
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


def add_new_answer(cursor, dict_of_new_answer):
    dict_of_new_answer = utils.add_submission_time(dict_of_new_answer)
    dict_of_new_answer = utils.add_missing_fields(dict_of_new_answer, HEADER_ANSWERS)
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s)
                    """,
                   dict_of_new_answer)


def add_question_view(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET view_number = view_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


def add_answer_upvote(cursor, _id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


def add_answer_downvote(cursor, _id):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = vote_number - 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


def add_question_upvote(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number + 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})


def add_question_downvote(cursor, _id):
    cursor.execute("""
                    UPDATE question
                    SET vote_number = vote_number - 1
                    WHERE id = %(_id)s;
                    """,
                   {"_id": _id})

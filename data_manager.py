import connection
import utils

HEADER_QUESTIONS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image"]
HEADER_COMMENTS = ["id", "question_id", "answer_id", "message", "submission_time", "edited_count"]


@connection.connection_handler
def get_all_questions(cursor):
    cursor.execute("""
                    SELECT id, submission_time, view_number, vote_number, title FROM question;
                    """)
    list_of_questions = cursor.fetchall()
    return list_of_questions


@connection.connection_handler
def get_latest_questions(cursor, how_many):
    cursor.execute("""
                    SELECT id, submission_time, title, view_number, vote_number FROM question
                    ORDER BY submission_time DESC
                    LIMIT %(number_of_rows)s;
                    """,
                   {"number_of_rows": how_many})
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
def get_last_question_by_title(cursor, question_title):
    cursor.execute("""
                    SELECT id FROM question
                    WHERE title = %(title)s
                    ORDER BY submission_time DESC
                    LIMIT 1;
                    """,
                   {"title": question_title})
    dict_of_id = cursor.fetchone()
    question_id = dict_of_id["id"]
    return question_id


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
def get_all_comments(cursor):
    cursor.execute("""
                    SELECT * FROM comment
                    """)
    list_of_comments = cursor.fetchall()
    return list_of_comments

@connection.connection_handler
def get_comments_by_question_id(cursor, _id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s
                    """,
                   {'question_id': _id})
    comment_for_question = cursor.fetchall()
    return comment_for_question

@connection.connection_handler
def add_new_comment(cursor, dict_of_new_comment):  # to be refactored
    dict_of_new_comment = utils.add_submission_time(dict_of_new_comment)
    dict_of_new_comment = utils.add_missing_fields(dict_of_new_comment, HEADER_COMMENTS)
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
                    """,
                   dict_of_new_comment)


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
                    WHERE id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})
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
def get_search_results(cursor, keyword):
    cursor.execute("""
                        SELECT * FROM question full join answer on question.id = answer.question_id
                          WHERE answer.message LIKE '%%' || %(keyword)s || '%%' OR question.message LIKE '%%' || %(keyword)s || '%%'
                         """, {'keyword': keyword})
    search_result = cursor.fetchall()
    return search_result

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


@connection.connection_handler
def get_question_id_for_answer(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id
                    FROM answer
                    WHERE id =%(answer_id)s;
                    """,
                   {"answer_id": answer_id})
    getting_id = cursor.fetchone()
    return getting_id["question_id"]





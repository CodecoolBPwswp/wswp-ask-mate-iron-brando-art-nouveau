import connection
import utils
from psycopg2 import sql

HEADER_QUESTIONS = ["id", "submission_time", "view_number", "vote_number", "title", "message", "image", "user_id"]
HEADER_ANSWERS = ["id", "submission_time", "vote_number", "question_id", "message", "image", "user_id"]
HEADER_COMMENTS = ["id", "question_id", "answer_id", "message", "submission_time", "edited_count"]
HEADER_USER = ["id", "registration_time", "email", "password_hash", "name", "last_login", "reputation"]


@connection.connection_handler
def get_all_questions(cursor, order_by="submission_time", order_direction="DESC"):
    if order_direction == "DESC":
        cursor.execute(
                sql.SQL("""
                        SELECT question.id, submission_time, view_number, vote_number, title, users.email AS author_email
                        FROM question JOIN users ON question.user_id = users.id
                        ORDER BY {} DESC;
                        """).format(sql.Identifier(order_by)))
    else:
        cursor.execute(
            sql.SQL("""
                    SELECT question.id, submission_time, view_number, vote_number, title, users.email AS author_email
                    FROM question JOIN users ON question.user_id = users.id
                    ORDER BY {} ASC
                    """).format(sql.Identifier(order_by))
        )
    list_of_questions = cursor.fetchall()
    return list_of_questions


@connection.connection_handler
def get_latest_questions(cursor, how_many):
    cursor.execute("""
                    SELECT question.id, submission_time, view_number, vote_number, title, users.email AS author_email
                    FROM question JOIN users ON question.user_id = users.id
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
def add_new_question(cursor, dict_of_new_question):
    dict_of_new_question = utils.add_submission_time(dict_of_new_question)
    counter_fields = ["vote_number", "view_number"]
    dict_of_new_question = utils.initialize_counter_fields(dict_of_new_question, counter_fields)
    dict_of_new_question["image"] = None  # to be refactored
    dict_of_new_question = utils.add_missing_fields(dict_of_new_question, HEADER_QUESTIONS)
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id) 
                    VALUES (%(submission_time)s, %(view_number)s, %(vote_number)s, %(title)s, %(message)s, %(image)s, %(user_id)s)
                    """,
                   dict_of_new_question)


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
def get_answer_comments_to_question(cursor, question_id):
    cursor.execute("""
                    SELECT answer.question_id, comment.answer_id, comment.submission_time, comment.message
                    FROM comment JOIN answer ON answer.id = comment.answer_id
                    WHERE answer.question_id = %(question_id)s
                    """,
                   {'question_id': question_id})
    list_of_comments = cursor.fetchall()
    return list_of_comments


@connection.connection_handler
def add_new_comment(cursor, dict_of_new_comment):
    dict_of_new_comment = utils.add_submission_time(dict_of_new_comment)
    dict_of_new_comment = utils.add_missing_fields(dict_of_new_comment, HEADER_COMMENTS)
    cursor.execute("""
                    INSERT INTO comment (question_id, answer_id, message, submission_time, edited_count)
                    VALUES (%(question_id)s, %(answer_id)s, %(message)s, %(submission_time)s, %(edited_count)s)
                    """,
                   dict_of_new_comment)


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
                    SELECT answer.id, submission_time, vote_number, question_id, message, users.email AS author_email
                    FROM answer JOIN users ON answer.user_id = users.id
                    WHERE question_id = %(question_id)s
                    ORDER BY id DESC
                    """,
                   {'question_id': _id})
    answers_for_question = cursor.fetchall()
    return answers_for_question


@connection.connection_handler
def get_search_results(cursor, keyword):
    cursor.execute("""
                        SELECT * FROM question full join answer on question.id = answer.question_id
                          WHERE answer.message LIKE %(keyword)s OR question.message LIKE %(keyword)s
                         """, {'keyword': '%' + keyword + '%'})

    search_result = cursor.fetchall()
    return search_result


@connection.connection_handler
def add_new_answer(cursor, dict_of_new_answer):  # to be refactored
    dict_of_new_answer = utils.add_submission_time(dict_of_new_answer)
    counter_fields = ["vote_number"]
    dict_of_new_answer = utils.initialize_counter_fields(dict_of_new_answer, counter_fields)
    dict_of_new_answer["image"] = None
    dict_of_new_answer = utils.add_missing_fields(dict_of_new_answer, HEADER_ANSWERS)
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                    VALUES (%(submission_time)s, %(vote_number)s, %(question_id)s, %(message)s, %(image)s, %(user_id)s)
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


@connection.connection_handler
def add_new_user(cursor, dict_of_new_user):
    saved_emails = get_all_user_emails()
    if dict_of_new_user["email"] in saved_emails:
        raise ValueError("Email already registered")
    dict_of_new_user = utils.store_password_hash(dict_of_new_user)
    counter_fields = ["reputation"]
    dict_of_new_user = utils.initialize_counter_fields(dict_of_new_user, counter_fields)
    dict_of_new_user["registration_time"] = utils.get_current_time()
    dict_of_new_user = utils.add_missing_fields(dict_of_new_user, HEADER_USER)
    cursor.execute("""
                    INSERT INTO users (registration_time, email, password_hash, name, last_login, reputation) 
                    VALUES (%(registration_time)s, %(email)s, %(password_hash)s, %(name)s, %(last_login)s, %(reputation)s)
                    """,
                   dict_of_new_user)


@connection.connection_handler
def get_password_hash_by_email(cursor, email):
    cursor.execute("""
                    SELECT password_hash FROM users
                    WHERE email = %s
                    """,
                   (email, ))
    try:
        saved_hash = cursor.fetchone()["password_hash"]
    except (KeyError, TypeError):
        saved_hash = ""
    return saved_hash


@connection.connection_handler
def get_users(cursor):
    cursor.execute("""
                    SELECT id,name,last_login,reputation
                    FROM users
                        """)
    user_list = cursor.fetchall()
    return user_list


@connection.connection_handler
def get_user_id_by_email(cursor, user_email):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE email = %s;
                    """,
                   (user_email, ))
    user_id = cursor.fetchone()["id"]
    return user_id


@connection.connection_handler
def get_user_email_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT email FROM users
                    WHERE id = %s;
                    """,
                   (user_id, ))
    user_id = cursor.fetchone()["email"]
    return user_id


@connection.connection_handler
def get_all_user_emails(cursor):
    cursor.execute("""
                    SELECT email FROM users
                    """)
    query_result = cursor.fetchall()
    list_of_emails = [row["email"] for row in query_result]
    return list_of_emails


@connection.connection_handler
def get_questions_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT id, submission_time, title, vote_number, view_number FROM question
                    WHERE user_id = %s
                    """,
                   (user_id, ))
    list_of_questions = cursor.fetchall()
    return list_of_questions

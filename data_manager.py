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
                        SELECT question.id, question.submission_time, view_number, question.vote_number, title, 
                            MAX(users.name) AS author, COUNT(a.id) AS number_of_answers FROM question 
                        JOIN users ON question.user_id = users.id
                        LEFT JOIN answer a on question.id = a.question_id
                        GROUP BY question.id
                        ORDER BY {} DESC;
                        """).format(sql.Identifier(order_by)))
    else:  # desc-asc in parameter
        cursor.execute(
            sql.SQL("""
                    SELECT question.id, question.submission_time, view_number, question.vote_number, title, 
                        MAX(users.name) AS author, COUNT(a.id) AS number_of_answers FROM question 
                    JOIN users ON question.user_id = users.id
                    LEFT JOIN answer a on question.id = a.question_id
                    GROUP BY question.id
                    ORDER BY {} ASC
                    """).format(sql.Identifier(order_by))
        )
    list_of_questions = cursor.fetchall()
    return list_of_questions


@connection.connection_handler
def get_latest_questions(cursor, how_many):
    cursor.execute("""
                    SELECT question.id, question.submission_time, view_number, question.vote_number, title, 
                        MAX(users.name) AS author, COUNT(a.id) AS number_of_answers FROM question 
                    JOIN users ON question.user_id = users.id
                    LEFT JOIN answer a on question.id = a.question_id
                    GROUP BY question.id
                    ORDER BY submission_time DESC
                    LIMIT %(number_of_rows)s;
                    """,  # limit into parameter of the previous query
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
                    SELECT comment.id, answer.question_id, comment.answer_id, comment.submission_time, comment.message
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
def delete_comment(cursor, comment_id):
    cursor.execute("""
                    DELETE from comment
                    WHERE id = %(comment_id)s
                    """,
                   {"comment_id": comment_id})

@connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})
    dict_of_comment = cursor.fetchone()
    return dict_of_comment


@connection.connection_handler
def update_comment(cursor, dict_of_updated_comment):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s
                    WHERE id = %(comment_id)s;
                    """,
                   {"message": dict_of_updated_comment["message"],
                    "comment_id": dict_of_updated_comment["id"]})



@connection.connection_handler
def get_question_id_by_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT question_id FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})
    result = cursor.fetchone()
    return result["question_id"]

@connection.connection_handler
def get_question_id_by_answer_comment_id(cursor, comment_id):
    cursor.execute("""
                    SELECT answer.question_id 
                    FROM answer
                    JOIN comment
                    ON comment.answer_id = answer.id
                    WHERE comment.id = %(comment_id)s;
                    """,
                   {"comment_id": comment_id})
    search_result = cursor.fetchone()
    return search_result["question_id"]


@connection.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT answer.question_id
                    FROM answer
                    JOIN comment
                    ON comment.answer_id = answer.id
                    WHERE answer.id = %(answer_id)s;
                    """,
                   {"answer_id": answer_id})
    search_result = cursor.fetchone()
    return search_result["question_id"]


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
                    SELECT answer.id, submission_time, vote_number, question_id, message, user_id, users.name AS author
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
                        SELECT question.id, question.submission_time, question.view_number, question.vote_number,
                                question.user_id, title, question.message
                        FROM question LEFT JOIN answer ON question.id = answer.question_id
                          WHERE answer.message ILIKE %(keyword)s 
                                OR question.message ILIKE %(keyword)s
                                OR question.title ILIKE %(keyword)s
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
def save_login_time(cursor, user_id):
    current_time = utils.get_current_time()
    cursor.execute("""
                    UPDATE users
                    SET last_login = %(login_time)s
                    WHERE id = %(user_id)s
                    """,
                   {"login_time": current_time, "user_id": user_id})


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
    query_result = cursor.fetchone()
    if query_result is None:
        return None
    else:
        return query_result["email"]


@connection.connection_handler
def get_user_data_by_id(cursor, user_id):
    cursor.execute("""
                    SELECT registration_time, email, name, last_login, reputation FROM users
                    WHERE id = %s
                    """,
                   (user_id, ))
    dict_of_user = cursor.fetchone()
    return dict_of_user


@connection.connection_handler
def get_user_data_by_email(cursor, user_email):
    cursor.execute("""
                    SELECT id, registration_time, email, name, last_login, reputation FROM users
                    WHERE email = %s
                    """,
                   (user_email, ))
    dict_of_user = cursor.fetchone()
    return dict_of_user


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
                    SELECT question.id, question.submission_time, title, question.vote_number, view_number, 
                        COUNT(a.id) AS number_of_answers 
                    FROM question LEFT JOIN answer a on question.id = a.question_id
                    WHERE question.user_id = %s
                    GROUP BY question.id
                    ORDER BY question.submission_time DESC
                    """,
                   (user_id, ))
    list_of_questions = cursor.fetchall()
    return list_of_questions


@connection.connection_handler
def get_answers_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT answer.id, answer.submission_time, answer.message, answer.vote_number, q.title AS question_title 
                    FROM answer JOIN question q on answer.question_id = q.id
                    WHERE answer.user_id = %s
                    ORDER BY answer.submission_time DESC
                    """,
                   (user_id, ))
    list_of_answers = cursor.fetchall()
    return list_of_answers

# MAGIC NUMBERS!!
@connection.connection_handler
def add_reputation_5(cursor,email):
    cursor.execute("""
                    UPDATE users
                      SET reputation = reputation + 5
                      WHERE email LIKE %s;
                    """,(email, ))



@connection.connection_handler
def add_reputation_10(cursor,email):
    cursor.execute("""
                    UPDATE users
                      SET reputation = reputation + 10
                      WHERE email LIKE %s;
                    """,(email, ))


@connection.connection_handler
def add_reputation_15(cursor,email):
    cursor.execute("""
                    UPDATE users
                      SET reputation = reputation + 15
                      WHERE email LIKE %s;
                    """,(email, ))


@connection.connection_handler
def minus_reputation_2(cursor,email):
    cursor.execute("""
                    UPDATE users
                      SET reputation = reputation - 2
                      WHERE email LIKE %s;
                    """,(email, ))

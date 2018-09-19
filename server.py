from flask import Flask, render_template, request, redirect, url_for, session
import data_manager
import utils

app = Flask(__name__)


@app.route('/')
def index():
    is_list_truncated = True
    number_of_questions_to_show = 5
    list_of_questions = data_manager.get_latest_questions(number_of_questions_to_show)
    return render_template('list.html', questions=list_of_questions, truncated=is_list_truncated)


@app.route('/list')
def route_list():
    is_list_truncated = False
    list_of_questions = data_manager.get_all_questions()
    return render_template('list.html', questions=list_of_questions, truncated=is_list_truncated)


@app.route('/list/order-by/<column>/<order>')
def order_questions(column, order):
    is_list_truncated = False
    list_of_questions = data_manager.get_all_questions(column, order)
    return render_template('list.html', questions=list_of_questions, truncated=is_list_truncated)


@app.route('/new_question')
def add_new_question():
    if "user" in session:
        return render_template('new_question.html')
    else:
        return redirect(url_for("index"))


@app.route('/new_question', methods=['POST'])
def save_new_question():
    dict_of_question = request.form.to_dict()
    dict_of_question["user_id"] = data_manager.get_user_id_by_email(session["user"])
    data_manager.add_new_question(dict_of_question)
    question_id = data_manager.get_last_question_by_title(dict_of_question["title"])
    question_page_url = url_for("get_question_details", question_id=question_id)
    return redirect(question_page_url)


@app.route('/questions/<question_id>')
def get_question_details(question_id):
    data_manager.add_question_view(question_id)
    question = data_manager.get_question_by_id(question_id)
    question_author = data_manager.get_user_email_by_id(question["user_id"])
    answers_for_question = data_manager.get_answers_by_question_id(question_id)
    comments_for_question = data_manager.get_comments_by_question_id(question_id)
    comments_for_answer = data_manager.get_answer_comments_to_question(question_id)
    return render_template("question_page.html", dict_of_question=question, question_author=question_author,
                           comments_for_question=comments_for_question, answers_to_list=answers_for_question,
                           comments_for_answer=comments_for_answer)


@app.route('/question-upvote', methods=["POST"])
def upvote_question():
    question_id = request.form["question_id"]
    data_manager.add_question_upvote(question_id)
    url_to_voted_question = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_voted_question)


@app.route('/question-downvote', methods=["POST"])
def downvote_question():
    question_id = request.form["question_id"]
    data_manager.add_question_downvote(question_id)
    url_to_voted_question = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_voted_question)


@app.route('/answer-upvote', methods=["POST"])
def upvote_answer():
    answer_id = request.form["answer_id"]
    data_manager.add_answer_upvote(answer_id)
    question_id = data_manager.get_question_id_for_answer(answer_id)
    url_to_question = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question)


@app.route('/answer-downvote', methods=["POST"])
def downvote_answer():
    answer_id = request.form["answer_id"]
    data_manager.add_answer_downvote(answer_id)
    question_id = data_manager.get_question_id_for_answer(answer_id)
    url_to_question = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question)


@app.route('/questions/<question_id>/new-comment')  # to be finished
def comment_to_question(question_id):
    instance_to_comment = "question"
    form_action = url_for('post_comment_to_question', question_id=question_id)
    question_to_comment = data_manager.get_question_by_id(question_id)
    return render_template("new_comment.html", dict_of_record=question_to_comment,
                           instance_to_comment=instance_to_comment, form_action=form_action)


@app.route('/details/<question_id>/new-comment', methods=["POST"])
def post_comment_to_question(question_id):
    dict_of_new_comment = request.form.to_dict()
    dict_of_new_comment["question_id"] = question_id
    data_manager.add_new_comment(dict_of_new_comment)
    url_to_question_details = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question_details)


@app.route('/answer/<answer_id>/new-comment')  # to be finished
def comment_to_answer(answer_id):
    form_action = url_for('post_comment_to_answer', answer_id=answer_id)
    answer_to_comment = data_manager.get_answer_by_id(answer_id)
    return render_template("new_comment.html", dict_of_record=answer_to_comment, form_action=form_action)


@app.route('/answer/<answer_id>/new-comment', methods=["POST"])
def post_comment_to_answer(answer_id):
    dict_of_new_comment = request.form.to_dict()
    dict_of_new_comment["answer_id"] = answer_id
    data_manager.add_new_comment(dict_of_new_comment)
    question_id = data_manager.get_question_id_for_answer(answer_id)
    url_to_question_details = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question_details)


@app.route('/details/<question_id>/new-answer')
def new_answer(question_id):
    if "user" not in session:
        return redirect(url_for("index"))
    question_to_answer = data_manager.get_question_by_id(question_id)
    question_author = data_manager.get_user_email_by_id(question_to_answer["user_id"])
    user_action = "Add new"
    form_action = url_for("post_answer", question_id=question_to_answer["id"])
    return render_template("new_answer.html", dict_of_question=question_to_answer,
                           dict_of_answer=None, user_action=user_action,
                           form_action=form_action, question_author=question_author)


@app.route('/details/<question_id>/new-answer', methods=["POST"])
def post_answer(question_id):
    dict_of_new_answer = request.form.to_dict()
    dict_of_new_answer["question_id"] = question_id
    dict_of_new_answer["user_id"] = data_manager.get_user_id_by_email(session["user"])
    data_manager.add_new_answer(dict_of_new_answer)
    url_to_question_details = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question_details)


@app.route('/answers/<answer_id>/edit-answer')
def edit_answer(answer_id):
    answer_to_edit = data_manager.get_answer_by_id(answer_id)
    dict_of_question = data_manager.get_question_by_id(answer_to_edit["question_id"])
    user_action = "Edit"
    form_action = url_for("save_edited_answer")
    return render_template('new_answer.html', dict_of_question=dict_of_question,
                           dict_of_answer=answer_to_edit, user_action=user_action,
                           form_action=form_action)


@app.route('/save-edited-answer', methods=["POST"])
def save_edited_answer():
    edited_message = request.form.to_dict()
    data_manager.update_answer(edited_message)
    edited_answer = data_manager.get_answer_by_id(edited_message["id"])
    url_to_question = url_for("get_question_details", postid=edited_answer["question_id"])
    return redirect(url_to_question)


@app.route('/search', methods=["POST"])
def search_question():
    keyword = request.form['search']
    search_result = data_manager.get_search_results(keyword)
    return render_template('search_results.html', keyword=keyword, search_result=search_result)


@app.route('/registration')
def register_user():
    form_action = url_for("save_new_user")
    user_action = "Sign up"
    return render_template("new_user.html", form_action=form_action, user_action=user_action)


@app.route('/registration', methods=["POST"])
def save_new_user():
    form_action = url_for("save_new_user")
    user_action = "Sign up"
    dict_of_new_user = request.form.to_dict()
    try:
        data_manager.add_new_user(dict_of_new_user)
    except ValueError:
        return render_template("new_user.html", form_action=form_action, user_action=user_action, registration_failed=True)
    return redirect(url_for("index"))


@app.route('/sign-in')
def sign_in_page():
    form_action = url_for("user_verification")
    user_action = "Sign in"
    return render_template("new_user.html", form_action=form_action, user_action=user_action)


@app.route('/sign-in', methods=["POST"])
def user_verification():
    attempt_email = request.form["email"]
    user_hash = data_manager.get_password_hash_by_email(attempt_email)  # invaild email?
    attempt_password = request.form["plain_text_password"]
    verified = utils.verify_password(attempt_password, user_hash)
    if verified:
        session["user"] = attempt_email
        return redirect(url_for("index"))
    else:
        form_action = url_for("user_verification")
        user_action = "Sign in"
        return render_template("new_user.html", form_action=form_action, user_action=user_action,
                               verification_failed=True)


@app.route('/', methods=["POST"])
def sign_out():
    session.pop("user")
    return redirect(url_for("index"))


@app.route('/list_users')
def list_users():
    if "user" not in session:
        return redirect(url_for("index"))
    user_list = data_manager.get_users()
    return render_template('user_list.html', user_list=user_list)


if __name__ == "__main__":
    app.secret_key = "Brandon_is_the_best"
    app.run(
        host="0.0.0.0",
        port=7550,
        debug=True
    )

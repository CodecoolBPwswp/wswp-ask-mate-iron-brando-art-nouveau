from flask import Flask, render_template, request, redirect, url_for
import data_manager
import utils

app = Flask(__name__)


@app.route('/')
def route_index():
    is_list_truncated = True
    number_of_questions_to_show = 5
    list_of_questions = data_manager.get_latest_questions(number_of_questions_to_show)
    return render_template('lists.html', questions=list_of_questions, truncated=is_list_truncated)


@app.route('/list')
def route_list():
    is_list_truncated = False
    user_questions = data_manager.get_all_questions()
    return render_template('lists.html', questions=user_questions, truncated=is_list_truncated)


@app.route('/list/order-by/<column>/<order>')
def order_questions(column, order):
    is_list_truncated = False
    list_of_questions = data_manager.get_all_questions(column, order)
    return render_template('lists.html', questions=list_of_questions, truncated=is_list_truncated)


@app.route('/new_question')
def add_new_question():
    return render_template('question_form.html')


@app.route('/new_question', methods=['POST'])
def save_new_question():
    dict_of_question = request.form.to_dict()
    data_manager.add_new_question(dict_of_question)  # not working
    question_id = data_manager.get_last_question_by_title(dict_of_question["title"])
    question_page_url = url_for("get_question_details", question_id=question_id)
    return redirect(question_page_url)


@app.route('/questions/<question_id>')
def get_question_details(question_id):
    data_manager.add_question_view(question_id)
    question = data_manager.get_question_by_id(question_id)
    answers_for_question = data_manager.get_answers_by_question_id(question_id)
    comments_for_question = data_manager.get_comments_by_question_id(question_id)
    comments_for_answer = data_manager.get_answer_comments_to_question(question_id)
    return render_template("question_page.html", dict_of_question = question, comments_for_question = comments_for_question,
                           answers_to_list = answers_for_question, comments_for_answer=comments_for_answer)


@app.route('/question-upvote', methods=["POST"])
def upvote_question():
    question_id = request.form["question_id"]
    data_manager.add_question_upvote(question_id)
    url_to_voted_question = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_voted_question)


@app.route('/question-downvote', methods = ["POST"])
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
    form_action = url_for('post_comment_to_question', postid=question_id)
    question_to_comment = data_manager.get_question_by_id(question_id)
    return render_template("comments.html", dict_of_record=question_to_comment,
                           distinguish = instance_to_comment, form_action=form_action)


@app.route('/details/<postid>/new-comment', methods = ["POST"])
def post_comment_to_question(postid):
    dict_of_new_comment = request.form.to_dict()
    dict_of_new_comment["question_id"] = postid
    data_manager.add_new_comment(dict_of_new_comment)
    url_to_question_details = url_for("get_question_details", question_id=postid)
    return redirect(url_to_question_details)


##### comment to answer

@app.route('/answer/<postid>/new-comment')  # to be finished
def comment_to_answer(postid):
    form_action = url_for('post_comment_to_answer', answer_id=postid)
    comment_to_answer = data_manager.get_answer_by_id(postid)
    return render_template("comments.html", dict_of_record=comment_to_answer, form_action=form_action)

@app.route('/answer/<answer_id>/new-comment', methods = ["POST"])
def post_comment_to_answer(answer_id):
    dict_of_new_comment = request.form.to_dict()
    dict_of_new_comment["answer_id"] = answer_id
    data_manager.add_new_comment(dict_of_new_comment)
    question_id = data_manager.get_question_id_for_answer(answer_id)
    url_to_question_details = url_for("get_question_details", question_id=question_id)
    return redirect(url_to_question_details)

#####




@app.route('/details/<postid>/new-answer')
def new_answer(postid):
    question_to_answer = data_manager.get_question_by_id(postid)
    user_action = "Add new"
    form_action = url_for("post_answer", postid=question_to_answer["id"])
    return render_template("answer.html", dict_of_question=question_to_answer,
                           dict_of_answer=None, user_action=user_action,
                           form_action=form_action)


@app.route('/details/<postid>/new-answer', methods = ["POST"])
def post_answer(postid):
    dict_of_new_answer = request.form.to_dict()
    dict_of_new_answer["question_id"] = postid
    data_manager.add_new_answer(dict_of_new_answer)
    url_to_question_details = url_for("get_question_details", question_id=postid)
    return redirect(url_to_question_details)


@app.route('/answers/<answer_id>/edit-answer')
def edit_answer(answer_id):
    answer_to_edit = data_manager.get_answer_by_id(answer_id)
    dict_of_question = data_manager.get_question_by_id(answer_to_edit["question_id"])
    user_action = "Edit"
    form_action = url_for("save_edited_answer")
    return render_template('answer.html', dict_of_question=dict_of_question,
                           dict_of_answer=answer_to_edit, user_action=user_action,
                           form_action=form_action)


@app.route('/save-edited-answer', methods=["POST"])
def save_edited_answer():
    edited_message = request.form.to_dict()
    data_manager.update_answer(edited_message)
    edited_answer = data_manager.get_answer_by_id(edited_message["id"])
    url_to_question = url_for("get_question_details", postid=edited_answer["question_id"])
    return redirect(url_to_question)


@app.route('/search', methods = ["POST","GET"])
def search_question():
    keyword = request.form['search']
    search_result = data_manager.get_search_results(keyword)
    return render_template('search_results.html', keyword=keyword, search_result = search_result)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7550,
        debug=True
    )

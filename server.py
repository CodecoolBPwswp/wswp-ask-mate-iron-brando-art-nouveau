from flask import Flask, render_template, request, redirect, url_for
import data_manager
import utils

app = Flask(__name__)


@app.route('/')
@app.route('/list')
def route_list():
    user_questions = data_manager.get_all_questions()
    return render_template('lists.html', questions=user_questions)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/form', methods=['POST'])
def save_question():
    dict_of_question = request.form.to_dict()
    data_manager.add_new_question(dict_of_question)  # not working
    question_id = data_manager.get_last_question_by_title(dict_of_question["title"])
    question_page_url = url_for("get_question_details", postid=question_id)
    return redirect(question_page_url)


@app.route('/details/<postid>')
def get_question_details(postid):
    data_manager.add_question_view(postid)
    question = data_manager.get_question_by_id(postid)
    answers_for_question = data_manager.get_answers_by_question_id(postid)
    comments_for_question = data_manager.get_comments_by_question_id(postid)
    return render_template("details.html", dict_of_question = question, comments_to_list = comments_for_question,
                           answers_to_list = answers_for_question)


@app.route('/details', methods = ["POST"])
def upvote_question():
    postid = request.form["post_id"]
    data_manager.add_question_upvote(postid)
    return redirect("/")


@app.route('/details_down', methods = ["POST"])
def downvote_question():
    postid = request.form["post_id"]
    data_manager.add_question_downvote(postid)
    return redirect("/")


@app.route('/comment/<postid>/new-comment')  # to be finished
def new_comment(postid):
    comment_to_answer = data_manager.get_question_by_id(postid)
    return render_template("comments.html", dict_of_question=comment_to_answer)

@app.route('/comment/<postid>/new-comment', methods = ["POST"])
def post_comment(postid):
    dict_of_new_comment = request.form.to_dict()
    dict_of_new_comment["question_id"] = postid
    data_manager.add_new_comment(dict_of_new_comment)
    url_to_question_details = url_for("get_question_details", postid=postid)
    return redirect(url_to_question_details)


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
    url_to_question_details = url_for("get_question_details", postid=postid)
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


    return render_template('search_results.html')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7550,
        debug=True
    )

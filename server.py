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
    dict_of_question["view_number"] = 0
    dict_of_question["vote_number"] = 0
    dict_of_question["image"] = None
    data_manager.add_new_question(dict_of_question)
    return redirect('/')


@app.route('/details/<postid>')
def get_question_details(postid):
    user_questions = data_manager.get_all_questions()
    data_manager.add_question_view(user_questions, postid)
    needed_post = utils.get_line_by_id(user_questions, postid)
    url_for_new_answer = url_for("new_answer", postid = postid)
    return render_template("details.html", postid = postid, needed_post = needed_post, url_for_new_answer = url_for_new_answer)


@app.route('/details', methods = ["POST"])
def voting_system_up():
    user_questions = data_manager.get_all_questions()
    postid = request.form["post_id"]
    data_manager.add_question_up_voting(user_questions, postid)
    

    return redirect("/")


@app.route('/details_down', methods = ["POST"])
def voting_system_down():
    user_questions = data_manager.get_all_questions()
    postid = request.form["post_id"]
    data_manager.add_question_down_voting(user_questions, postid)
    

    return redirect("/")


@app.route('/details/<postid>/new-answer')
def new_answer(postid):
    user_questions = data_manager.get_all_questions()
    return render_template("answer.html", question = user_questions)


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

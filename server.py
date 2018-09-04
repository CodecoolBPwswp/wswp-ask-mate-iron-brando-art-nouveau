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
    question_id = data_manager.add_new_question(dict_of_question)
    return redirect(url_for("get_question_details",postid=question_id))


@app.route('/details/<postid>')
def get_question_details(postid):
    user_questions = data_manager.get_all_questions()
    data_manager.add_question_view(user_questions, postid)
    needed_post = utils.get_line_by_id(user_questions, postid)
    url_for_new_answer = url_for("new_answer", postid = postid)
    all_answers = data_manager.get_all_answers()
    answers_for_question = utils.get_line_by_id(all_answers, postid, field_to_check="question_id", as_list=True)
    return render_template("details.html", postid = postid, needed_post = needed_post,
                           url_for_new_answer = url_for_new_answer, answers_to_list = answers_for_question)


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
    question_to_answer = utils.get_line_by_id(user_questions, postid)
    return render_template("answer.html", questions = question_to_answer)


@app.route('/details/<postid>/new-answer', methods = ["POST"])
def post_answer(postid):
    dict_of_new_answer = request.form.to_dict()
    dict_of_new_answer["vote_number"] = 0
    dict_of_new_answer["image"] = None
    dict_of_new_answer["question_id"] = postid
    data_manager.add_new_answer(dict_of_new_answer)
    return redirect(url_for("get_question_details", postid=postid))


@app.route('/search', methods = ["POST","GET"])
def get_answer_to_qeustion():


    return render_template('search_results.html')



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

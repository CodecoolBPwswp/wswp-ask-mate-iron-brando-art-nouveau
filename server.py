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
    question_id = data_manager.add_new_question(dict_of_question)  # not working
    question_page_url = url_for("get_question_details", postid=question_id)
    return redirect(question_page_url)


@app.route('/details/<postid>')
def get_question_details(postid):
    data_manager.add_question_view(postid)
    question = data_manager.get_question_by_id(postid)
    answers_for_question = data_manager.get_answers_by_question_id(postid)
    return render_template("details.html", dict_of_question = question,
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
    user_questions = data_manager.get_all_questions()  # might want to use something else
    comment_to_answer = utils.get_line_by_id(user_questions, postid)
    return render_template("comments.html", questions=comment_to_answer)


@app.route('/details/<postid>/new-answer')
def new_answer(postid):
    question_to_answer = data_manager.get_question_by_id(postid)
    return render_template("answer.html", dict_of_question=question_to_answer)


@app.route('/details/<postid>/new-answer', methods = ["POST"])
def post_answer(postid):
    dict_of_new_answer = request.form.to_dict()
    dict_of_new_answer["question_id"] = postid
    data_manager.add_new_answer(dict_of_new_answer)
    url_to_question_details = url_for("get_question_details", postid=postid)
    return redirect(url_to_question_details)


@app.route('/search', methods = ["POST","GET"])
def search_question():
    keyword = request.form['search']
    search_result = data_manager.get_search_results(keyword)
    print('a' + search_result)
    return render_template('search_results.html', keyword=keyword, search_result = search_result)



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


# routing functions here
@app.route('/', methods=['POST',"GET"])
@app.route('/list')
def route_list():
    user_questions = data_manager.get_all_questions()
    return render_template('lists.html', questions=user_questions)


@app.route('/form', methods=["GET"])
def form():
    return render_template('form.html')


@app.route('/form', methods=['POST'])
def save_question():
    dict_of_question = request.form.to_dict()
    dict_of_question["view_number"] = None
    dict_of_question["image"] = None
    data_manager.add_new_question(dict_of_question)
    return redirect('/')


@app.route('/details/<postid>', methods=("GET","POST"))
def get_question_details(postid):
    user_questions = data_manager.get_all_questions()
    needed_post = data_manager.get_line_by_id(user_questions, postid)
    

    return render_template("details.html", postid = postid, needed_post = needed_post)


@app.route('/cancel')
def cancel():
    return('/')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

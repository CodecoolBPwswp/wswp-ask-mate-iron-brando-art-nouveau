from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


# routing functions here
@app.route('/', methods=['POST',"GET"])
@app.route('/list')
def route_list():
    user_questions = data_manager.get_all_questions()

    return render_template('lists.html', questions=user_questions)


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/details')
def get_question_details():
    user_questions = data_manager.get_all_questions()
    return render_template("details.html", questions=user_questions)


@app.route('/cancel')
def cancel():
    return('/')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

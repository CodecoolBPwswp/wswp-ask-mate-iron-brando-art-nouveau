from flask import Flask, render_template, request, redirect, url_for
import data_manager

app = Flask(__name__)


# routing functions here
@app.route('/', methods=['POST',"GET"])
@app.route('/list')
def route_list():
    user_questions = data_manager.get_data_from_file("questions")

    return render_template('lists.html', user_questions=user_questions)




if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

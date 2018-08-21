from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# routing functions here
@app.route('/', methods=['POST',"GET"])
@app.route('/list')
def route_list():
    user_questions = data_manager.TBC()

    return render_template('list.html', user_questions=user_questions)


@app.route('/')
def form():
    return render_template('form.html')

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

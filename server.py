from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# routing functions here


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=7000,
        debug=True
    )

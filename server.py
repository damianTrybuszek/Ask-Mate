from flask import Flask, render_template
import data_handling

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello !"

@app.route("/list")
def list():
    question_list = data_handling.get_questions()
    headers = data_handling.get_headers()
    return render_template("list.html", question_list=question_list, headers=headers)


@app.route("/question/question_id")
def display():
    question_list = data_handling.get_questions()
    question_id = 


if __name__ == "__main__":
    app.run(debug=True)
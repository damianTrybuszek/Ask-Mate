from flask import Flask, render_template, request, redirect, url_for
import data_handling
import util as util

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello !"

@app.route("/list")
def list():
    question_list = data_handling.get_questions()
    headers = data_handling.get_headers_questions()
    return render_template("list.html", question_list=question_list, headers=headers)


@app.route("/question/<question_id>")
def display(question_id):
    question_list = data_handling.get_questions()
    answer_list = data_handling.get_answers()
    headers = data_handling.get_headers_questions()
    answers_to_questions = []
    if question_id:
        question_to_display = "0"
        for question in question_list:
            if question["id"] == question_id:
                question_to_display = question
        headers = data_handling.get_headers_questions()

    if question_id !=0:
        for answer in answer_list:
            if answer["question_id"] == question_id:
                temp_list = [answer["vote_number"], answer["message"]]
                answers_to_questions.append(temp_list)

        if len(answers_to_questions) > 0:
            data_handling.bubble_sort(answers_to_questions)

    return render_template("display.html", question=question_to_display, answers=answers_to_questions, headers=headers)


@app.route("/add_question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        new_question_input = dict(request.form)
        data_handling.save_question(new_question_input)
        return redirect(f"/question/{new_question_input['id']}")
    return render_template("add_question.html")

if __name__ =="__main__":
    app.run(debug=True)
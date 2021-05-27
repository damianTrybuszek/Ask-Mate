from flask import Flask, render_template, request, redirect, url_for, flash
import data_handling as data_handling
import util as util
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = data_handling.UPLOAD_FOLDER

@app.route("/")
def hello():
    return render_template('index.html')


@app.route("/list", methods=["POST", "GET"])
def list():
    order_by = request.args.get('order_by', 'id')
    order_direction = request.args.get('order_direction', 'desc')
    headers = data_handling.get_headers_questions()
    question_list = data_handling.get_questions(order_by, order_direction)

    return render_template("list.html", question_list=question_list, headers=headers)


@app.route("/question/<question_id>", methods=["POST", "GET"])
def display(question_id):
    order_by = request.args.get('order_by', 'vote_number')
    order_direction = request.args.get('order_direction', 'asc')
    headers = data_handling.get_headers_answers()
    answer_list = util.get_answer_to_display(question_id, order_by, order_direction)
    question = util.get_questions_to_display(question_id)

    if len(question) > 0:
        question_to_display = question[0]
    else:
        question_to_display = question

    return render_template("display.html", question=question_to_display, answers=answer_list, headers=headers)


@app.route("/add_question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        if "file" in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            if filename:
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                filename = False
        new_question_input = dict(request.form)
        data_handling.save_question(new_question_input, filename)
        question_id = data_handling.get_last_question()[0]['id']
        return redirect(f"/question/{question_id}")
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def post_an_answer(question_id):
    if request.method == "POST":
        if "file" in request.files:
            file = request.files['file']
            filename = secure_filename(file.filename)
            if filename:
                filename = str(question_id) + "_" + filename
                file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            else:
                filename = False
        answer = dict(request.form)
        data_handling.save_answer(question_id, answer, filename)
        return redirect( f"/question/{answer['question_id']}")
    return render_template("post_an_answer.html", question_id=question_id)


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = data_handling.get_question_by_id(question_id)[0]
    if request.method == "POST":
        new_data = dict(request.form)
        data_handling.overwrite_question(question_id, new_data)
        return redirect(f"/question/{question_id}")
    return render_template("edit_question.html", question=question, question_id=question_id)

@app.route("/answer/<answer_id>/edit", methods=["GET", "POST"])
def edit_answer(answer_id):
    answer = data_handling.get_answer_by_id(answer_id)[0]
    question_id = answer['question_id']
    question = data_handling.get_question_by_id(question_id)[0]

    if request.method == "POST":
        new_data = dict(request.form)
        data_handling.overwrite_answer(answer_id, new_data)
        return redirect(f"/question/{question_id}")
    return render_template("edit_answer.html", answer=answer, question=question)


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    deleted_answer = data_handling.get_answer_by_id(answer_id)[0]
    if deleted_answer:
        if request.method == "POST":
            if 'yes_button' in request.form:
                data_handling.delete_answer(deleted_answer)
                return redirect(f"/question/{deleted_answer['question_id']}")
            else:
                return redirect(f"/question/{deleted_answer['question_id']}")
        return render_template("delete_answer.html", answer_id=answer_id)
    else:
        return render_template("wrong_answer_id.html")


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    deleted_question = data_handling.get_question_by_id(question_id)[0]
    if deleted_question:
        try:
            if request.method == "POST":
                if 'yes_button' in request.form:
                    data_handling.delete_question(deleted_question)
                    return redirect("/list")
                else:
                    return redirect(f"/question/{deleted_question['id']}")
            return render_template("delete_question.html", question_id=question_id)
        except:
            raise KeyError("This question still has answers that are tied to it, you can't just delete it")
    else:
        return render_template("wrong_question_id.html")


@app.route("/question/<question_id>/vote_up", methods=["GET", "POST"])
def questions_vote_up(question_id):
    question = data_handling.get_question_by_id(question_id)
    if request.method == "POST":
        if 'vote_up' in request.form:
            data_handling.question_vote_up(question)
    return redirect("/list")


@app.route("/question/<question_id>/vote_down", methods=["GET", "POST"])
def questions_vote_down(question_id):
    question = data_handling.get_question_by_id(question_id)
    if request.method == "POST":
        if 'vote_down' in request.form:
            data_handling.question_vote_down(question)
    return redirect("/list")


@app.route("/answer/<answer_id>/vote_up", methods=["GET", "POST"])
def answers_vote_up(answer_id):
    answer = data_handling.get_answer_by_id(answer_id)
    if request.method == "POST":
        if 'vote_up' in request.form:
            data_handling.answer_vote_up(answer)
    return redirect(f"/question/{answer[0]['question_id']}")


@app.route("/answer/<answer_id>/vote_down", methods=["GET", "POST"])
def answers_vote_down(answer_id):
    answer = data_handling.get_answer_by_id(answer_id)
    if request.method == "POST":
        if 'vote_down' in request.form:
            data_handling.answer_vote_down(answer)
    return redirect(f"/question/{answer[0]['question_id']}")


if __name__ == "__main__":
    app.run(debug=True)
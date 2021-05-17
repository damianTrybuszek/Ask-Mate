from flask import Flask, render_template, request, redirect, url_for
import data_handling as data_handling
import util as util

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/list", methods=["POST", "GET"])
def list():
    question_list = data_handling.get_questions()
    headers = data_handling.get_headers_questions()
    order_by = request.args.get('order_by', None)
    order_direction = request.args.get('order_direction', None)
    question_list = util.sort_table(order_by, order_direction, question_list)
    question_list_to_show = util.get_question_list_with_real_time(question_list)
    return render_template("list.html", question_list=question_list_to_show, headers=headers)

@app.route("/question/<question_id>")
def display(question_id):
    question_to_display, headers = util.get_questions_to_display(question_id)
    final_answer_list = util.get_answer_to_display(question_id)
    return render_template("display.html", question=question_to_display, answers=final_answer_list, headers=headers)

@app.route("/add_question", methods=["POST", "GET"])
def add_question():
    if request.method == "POST":
        new_question_input = dict(request.form)
        data_handling.save_question(new_question_input)
        return redirect(f"/question/{new_question_input['id']}")
    return render_template("add_question.html")


@app.route("/question/<question_id>/new-answer", methods=["GET", "POST"])
def post_an_answer(question_id):
    if request.method == "POST":
        answer = dict(request.form)
        data_handling.save_answer(question_id, answer)
        return redirect( f"/question/{answer['question_id']}")
    return render_template("post_an_answer.html", question_id=question_id)


@app.route("/question/<question_id>/edit", methods=["GET", "POST"])
def edit_question(question_id):
    question = data_handling.get_question_by_id(question_id)
    if request.method == "POST":
        new_data = dict(request.form)
        util.edit_single_question(question, new_data)
        data_handling.overwrite_question(question)
        return redirect( f"/question/{question_id}")
    return render_template("edit_question.html", question=question, question_id=question_id)


@app.route("/answer/<answer_id>/delete", methods=["GET", "POST"])
def delete_answer(answer_id):
    answer = data_handling.get_answer_by_id(answer_id)
    if request.method == "POST":
        if 'yes_button' in request.form:
            data_handling.delete_answer(answer)
            return redirect(f"/question/{answer['question_id']}")
        else:
            return redirect(f"/question/{answer['question_id']}")

    return render_template("delete_answer.html", answer_id=answer_id)


@app.route("/question/<question_id>/delete", methods=["GET", "POST"])
def delete_question(question_id):
    question = data_handling.get_question_by_id(question_id)
    if request.method == "POST":
        if 'yes_button' in request.form:
            data_handling.delete_question(question)
            return redirect("/list")
        else:
            return redirect(f"/question/{question['id']}")

    return render_template("delete_question.html", question_id=question_id)


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
    return redirect("/list")

@app.route("/answer/<answer_id>/vote_down", methods=["GET", "POST"])
def answers_vote_down(answer_id):
    answer = data_handling.get_answer_by_id(answer_id)
    if request.method == "POST":
        if 'vote_down' in request.form:
            data_handling.answer_vote_down(answer)
    return redirect("/list")


if __name__ == "__main__":
    app.run(debug=True)
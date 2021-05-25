import time
import data_handling as data_handling
from datetime import datetime
import copy


def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)


def get_real_time(unix_time):
    return datetime.fromtimestamp(int(unix_time))


def sort_table(order_by, order_direction, questions_list):
    if order_direction == "asc":
        direction = False
    else:
        direction = True

    return sorted(questions_list, key=lambda x: x[order_by], reverse=direction)


def edit_single_question(question, new_data):
    for key in new_data:
        question[key] = new_data[key]


def question_vote_up(question):
    temp_vote_number = int(question["vote_number"]) + 1
    question["vote_number"] = str(temp_vote_number)


def question_vote_down(question):
    temp_vote_number = int(question["vote_number"]) - 1
    question["vote_number"] = str(temp_vote_number)


def get_questions_to_display(question_id):
    question_list = data_handling.get_questions()
    if question_id:
        question_to_display = "0"
        for question in question_list:
            if question["id"] == question_id:
                question_to_display = question
    return question_to_display


def get_answer_to_display(question_id):
    answers_to_questions = []
    answer_list = data_handling.get_answers()
    if question_id != 0:
        for answer in answer_list:
            if answer["question_id"] == question_id:
                answers_to_questions.append(answer)

    return answers_to_questions


def get_question_list_with_real_time(question_list):
    new_question_list = copy.deepcopy(question_list)
    for element in new_question_list:
        element["submission_time"] = get_real_time(element["submission_time"])
    return new_question_list




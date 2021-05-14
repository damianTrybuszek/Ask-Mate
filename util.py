import time
import data_handling as data_handling

def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)

def get_question_to_display(question_id):
    question_list = data_handling.get_questions()
    answers_to_questions = []
    if question_id:
        question_to_display = "0"
        for question in question_list:
            if question["id"] == question_id:
                return question

def get_answers(question_id):
    answers_to_questions = []
    answer_list = data_handling.get_answers()
    if question_id != 0:
        for answer in answer_list:
            if answer["question_id"] == question_id:
                temp_list = [answer["vote_number"], answer["message"]]
                answers_to_questions.append(temp_list)
    if len(answers_to_questions) > 0:
        data_handling.bubble_sort(answers_to_questions)
    return answers_to_questions
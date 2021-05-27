import time
import data_handling as data_handling
from datetime import datetime
import copy
import database_connection as database_connection


def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)


def get_real_time(unix_time):
    return datetime.fromtimestamp(int(unix_time))


# def sort_table(order_by, order_direction, questions_list):
#     if order_direction == "asc":
#         direction = False
#     else:
#         direction = True
#
#     return sorted(questions_list, key=lambda x: x[order_by], reverse=direction)


def question_vote_up(question):
    temp_vote_number = int(question["vote_number"]) + 1
    question["vote_number"] = str(temp_vote_number)


def question_vote_down(question):
    temp_vote_number = int(question["vote_number"]) - 1
    question["vote_number"] = str(temp_vote_number)


@database_connection.connection_handler
def get_questions_to_display(cursor, question_id):
    # question_list = data_handling.get_questions()
    # if question_id:
    #     question_to_display = "0"
    #     for question in question_list:
    #         if question["id"] == question_id:
    #             question_to_display = question
    # return question_to_display
    query = """
            SELECT *
            FROM question
            WHERE id = %s;
            """
    query_params = [question_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_to_display(cursor, question_id, order_by, order_direction):
    # answers_to_questions = []
    # answer_list = data_handling.get_answers()
    # if question_id != 0:
    #     for answer in answer_list:
    #         if answer["question_id"] == question_id:
    #             answers_to_questions.append(answer)
    #
    # return answers_to_questions
    query = f"SELECT * FROM answer WHERE question_id = {question_id} ORDER BY {order_by} {order_direction};"
    cursor.execute(query)
    return cursor.fetchall()


def get_question_list_with_real_time(question_list):
    new_question_list = copy.deepcopy(question_list)
    for element in new_question_list:
        element["submission_time"] = get_real_time(element["submission_time"])
    return new_question_list




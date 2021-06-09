import time
import data_handling as data_handling
from datetime import datetime
import copy
import database_connection as database_connection
import bcrypt

def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)


def get_real_time(unix_time):
    return datetime.fromtimestamp(int(unix_time))


def question_vote_up(question):
    temp_vote_number = int(question["vote_number"]) + 1
    question["vote_number"] = str(temp_vote_number)


def question_vote_down(question):
    temp_vote_number = int(question["vote_number"]) - 1
    question["vote_number"] = str(temp_vote_number)


@database_connection.connection_handler
def get_questions_to_display(cursor, question_id):
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
    query = f"SELECT id, message, image, vote_number, submission_time, question_id FROM answer WHERE question_id = {question_id} ORDER BY {order_by} {order_direction};"
    cursor.execute(query)
    return cursor.fetchall()


def get_question_list_with_real_time(question_list):
    new_question_list = copy.deepcopy(question_list)
    for element in new_question_list:
        element["submission_time"] = get_real_time(element["submission_time"])
    return new_question_list


def text_highlighted(question_list, search_phrase, column):
    for element in question_list:
        if str(search_phrase.lower()) in (element[column]).lower():
            element[column] = element[column].replace(search_phrase, f"<mark>{search_phrase}</mark>")
    return question_list


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('UTF-8'), salt)
    return hashed_password.decode('UTF-8')

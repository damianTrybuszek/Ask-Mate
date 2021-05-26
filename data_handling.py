import os
import csv
import util as util
import database_connection as database_connection


# DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\question.csv'
# DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\answer.csv'
UPLOAD_FOLDER = os.getcwd() + "\\static\\img\\"

# def file_overwrite(iterable, headers, filename):
#     with open(filename, 'w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
#         file.write(",".join(headers)+"\n")
#         for item in iterable:
#             writer.writerow(item)


@database_connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = f"SELECT * FROM question ORDER BY {order_by} {order_direction};"
    # query_params = [order_by, order_direction]
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_by_id(cursor, question_id):
    # questions_list = get_questions()
    # for question in questions_list:
    #     if question['id'] == question_id:
    #         return question
    # return None
    query = """
            SELECT *
            FROM question
            WHERE id = %s
            ORDER BY id;
            """
    query_params = [question_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_by_id(cursor, answer_id):
    # answers_list = get_answers()
    # for answer in answers_list:
    #     if answer['id'] == answer_id:
    #         return answer
    # return None
    query = """
            SELECT *
            FROM answer
            WHERE id = %s;
            """
    query_params = [answer_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def get_headers_questions(cursor):
    # with open(DATA_FILE_PATH_QUESTIONS) as file:
    #     lines = file.readlines()
    #     return lines[0].replace("\n", "").split(",")
    query = """
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'question';
            """
    cursor.execute(query)
    headers = cursor.fetchall()
    final_headers_list = []
    for dictionary in headers:
        for key in dictionary:
            final_headers_list.append(dictionary[key])
    return final_headers_list


@database_connection.connection_handler
def get_headers_answers(cursor):
#     with open(DATA_FILE_PATH_ANSWERS) as file:
#         lines = file.readlines()
#         return lines[0].replace("\n", "").split(",")
    query = """
            SELECT column_name
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = 'answer';
            """
    cursor.execute(query)
    headers = cursor.fetchall()
    final_headers_list = []
    for dictionary in headers:
        for key in dictionary:
            final_headers_list.append(dictionary[key])

    return final_headers_list


@database_connection.connection_handler
def get_answers(cursor):
    # answer_list = []
    # with open(DATA_FILE_PATH_ANSWERS) as file:
    #     reader = csv.DictReader(file)
    #     for row in reader:
    #         answer_list.append(row)
    # return answer_list
    query = """
            SELECT *
            FROM answer
            ORDER BY id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def save_question(cursor, new_question_input, filename):
    # data_questions = get_questions()
    # new_question_input["id"] = str(int(get_max_id(data_questions)) + 1)
    new_question_input["submission_time"] = str(util.get_real_time((util.get_unix_timestamp())))
    new_question_input["view_number"] = "0"
    new_question_input["vote_number"] = "0"
    if filename:
        new_question_input['image'] = filename
    else:
        new_question_input['image'] = None

    # with open(DATA_FILE_PATH_QUESTIONS, 'a', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=get_headers_questions(), delimiter=",")
    #     writer.writerow(new_question_input)
    query = """
            INSERT INTO question
            (submission_time, view_number, vote_number, title, message, image)
            VALUES 
            (%s, %s, %s, %s, %s, %s);
            """
    query_params = [new_question_input['submission_time'], new_question_input['view_number'],
                    new_question_input['vote_number'], new_question_input['title'],
                    new_question_input['message'], new_question_input['image']]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def save_answer(cursor, question_id, new_answer, filename):
    # data_list = get_answers()
    new_answer["submission_time"] = str(util.get_real_time((util.get_unix_timestamp())))
    new_answer['vote_number'] = "0"
    new_answer['question_id'] = question_id
    if filename:
        new_answer['image'] = filename
    else:
        new_answer['image'] = None
    # with open(DATA_FILE_PATH_ANSWERS, 'a', newline='') as file:
    #     writer = csv.DictWriter(file, fieldnames=get_headers_answers(), delimiter=",")
    #     writer.writerow(answer)
    query = """
            INSERT INTO answer
            (submission_time, vote_number, question_id, message, image) 
            VALUES 
            (%s, %s, %s, %s, %s);
            """
    query_params = [new_answer['submission_time'], new_answer['vote_number'],
                    new_answer['question_id'], new_answer['message'],
                    new_answer['image']]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def overwrite_question(cursor, amended_question):
    # questions_list = get_questions()
    # for i in range(len(questions_list)):
    #     if questions_list[i]['id'] == question['id']:
    #         questions_list[i]['message'] = question['message']
    #         questions_list[i]['title'] = question['title']
    # headers = get_headers_questions()
    # file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)
    query = """
            UPDATE question
            SET title = %s,
            message = %s,
            WHERE id = %s;
            """
    query_params = [amended_question['title'], amended_question['message'], amended_question['id']]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def delete_answer(cursor, deleted_answer):
    # answers_list = get_answers()
    # headers = get_headers_answers()
    # for i in range(len(answers_list)):
    #     if answers_list[i]['id'] == answer['id']:
    #         if len(answers_list[i]['image']) > 0:
    #             os.remove(f"{UPLOAD_FOLDER}/{answers_list[i]['image']}")
    #
    #         answers_list.pop(i)
    #         break
    #
    # file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)
    if deleted_answer['image']:
        os.remove(f"{UPLOAD_FOLDER}/{deleted_answer['image']}")

    query = """
            DELETE from answer
            WHERE id = %s;
            """
    query_params = [deleted_answer['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def delete_question(cursor, deleted_question):
    # questions_list = get_questions()
    # headers = get_headers_questions()
    # for i in range(len(questions_list)):
    #     if questions_list[i]['id'] == question['id']:
    #         if len(questions_list[i]['image']) > 0:
    #             os.remove(f"{UPLOAD_FOLDER}/{questions_list[i]['image']}")
    #         questions_list.pop(i)
    #         break
    #
    # file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)

    if deleted_question['image']:
        os.remove(f"{UPLOAD_FOLDER}/{deleted_question['image']}")

    query = """
            DELETE from question
            WHERE id = %s;
            """
    query_params = [deleted_question['id']]
    cursor.execute(query, query_params)

# def get_max_id(iterable_of_dicts):
#     if len(iterable_of_dicts) <= 0:
#         return 1
#     max_id = 0
#     max_index = 0
#     for index, element in enumerate(iterable_of_dicts):
#         if int(element['id']) > max_id:
#             max_id = int(element['id'])
#             max_index = index
#     return iterable_of_dicts[max_index]['id']


@database_connection.connection_handler
def question_vote_up(cursor, voted_question):
    # questions_list = get_questions()
    # headers = get_headers_questions()
    # for element in questions_list:
    #     if element['id'] == question['id']:
    #         temp_vote_number = int(element["vote_number"]) + 1
    #         element["vote_number"] = str(temp_vote_number)
    # file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)

    query = """
            UPDATE question
            SET vote_number = vote_number + 1
            WHERE id = %s;
            """
    query_params = [voted_question['id']]
    cursor.execute(query, query_params)

    return cursor.fetchall()

@database_connection.connection_handler
def question_vote_down(cursor, voted_question):
    # questions_list = get_questions()
    # headers = get_headers_questions()
    # for element in questions_list:
    #     if element['id'] == question['id']:
    #         temp_vote_number = int(element["vote_number"]) - 1
    #         element["vote_number"] = str(temp_vote_number)
    # file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)

    query = """
            UPDATE question
            SET vote_number = vote_number - 1
            WHERE id = %s;
            """
    query_params = [voted_question['id']]
    cursor.execute(query, query_params)

    return cursor.fetchall()


@database_connection.connection_handler
def answer_vote_up(cursor, voted_answer):
    # answers_list = get_answers()
    # headers = get_headers_answers()
    # for element in answers_list:
    #     if element['id'] == answer['id']:
    #         temp_vote_number = int(element["vote_number"]) + 1
    #         element["vote_number"] = str(temp_vote_number)
    # file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)

    query = """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = %s;
            """
    query_params = [voted_answer['id']]
    cursor.execute(query, query_params)

    return cursor.fetchall()


@database_connection.connection_handler
def answer_vote_down(cursor, voted_answer):
    # answers_list = get_answers()
    # headers = get_headers_answers()
    # for element in answers_list:
    #     if element['id'] == answer['id']:
    #         temp_vote_number = int(element["vote_number"]) - 1
    #         element["vote_number"] = str(temp_vote_number)
    # file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)

    query = """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = %s;
            """
    query_params = [voted_answer['id']]
    cursor.execute(query, query_params)

    return cursor.fetchall()
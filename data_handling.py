import os
import util as util
import database_connection as database_connection
from psycopg2 import sql

UPLOAD_FOLDER = os.getcwd() + "\\static\\img\\"


@database_connection.connection_handler
def get_questions(cursor, order_by, order_direction):
    query = f"SELECT * FROM question ORDER BY {order_by} {order_direction};"
    # query_params = [order_by, order_direction] - won't work for some reason
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
            SELECT *
            FROM question
            WHERE id = %s;
            """
    query_params = [question_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def get_answer_by_id(cursor, answer_id):
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
    query = """
            SELECT *
            FROM answer
            ORDER BY id;
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def save_question(cursor, new_question_input, filename):
    new_question_input["submission_time"] = str(util.get_real_time((util.get_unix_timestamp())))
    new_question_input["view_number"] = "0"
    new_question_input["vote_number"] = "0"
    if filename:
        new_question_input['image'] = filename
    else:
        new_question_input['image'] = None
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

    
@database_connection.connection_handler
def get_last_question(cursor):
    query = """
            SELECT * FROM question
            ORDER BY id DESC LIMIT 1; 
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def save_answer(cursor, question_id, new_answer, filename):
    new_answer["submission_time"] = str(util.get_real_time((util.get_unix_timestamp())))
    new_answer['vote_number'] = "0"
    new_answer['question_id'] = question_id
    if filename:
        new_answer['image'] = filename
    else:
        new_answer['image'] = None

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


@database_connection.connection_handler
def overwrite_question(cursor, question_id, new_data):
    query = """
            UPDATE question
            SET
            title = %s,
            message = %s
            WHERE id = %s;
            """
    query_params = [new_data['title'], new_data['message'], question_id]
    cursor.execute(query, query_params)

    
@database_connection.connection_handler
def overwrite_answer(cursor, answer_id, new_data):
    query = """
            UPDATE answer
            SET
            message = %s
            WHERE id = %s;
            """
    query_params = [new_data['message'], answer_id]
    cursor.execute(query, query_params)

    
@database_connection.connection_handler
def delete_answer(cursor, deleted_answer):
    if deleted_answer['image']:
        os.remove(f"{UPLOAD_FOLDER}/{deleted_answer['image']}")

    query = """
            DELETE from answer
            WHERE id = %s;
            """
    query_params = [deleted_answer['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def delete_all_comments_from_question(cursor, question_id):
    query = sql.SQL("DELETE FROM comment WHERE question_id=%s")
    query_params = [int(question_id)]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def delete_all_answers_comments_from_question(cursor, question_id):
    query = sql.SQL("DELETE FROM comment USING answer WHERE answer.id = comment.answer_id AND answer.question_id=%s")
    query_params = [int(question_id)]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def delete_all_answers_from_question(cursor, question_id):
    query = sql.SQL("DELETE FROM answer WHERE question_id=%s")
    query_params = [int(question_id)]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def delete_question(cursor, deleted_question):
    if deleted_question['image']:
        os.remove(f"{UPLOAD_FOLDER}/{deleted_question['image']}")

    query = """
            DELETE from question
            WHERE id = %s;
            """
    query_params = [deleted_question['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def question_vote_up(cursor, voted_question):
    query = """
            UPDATE question
            SET vote_number = vote_number + 1
            WHERE id = %s;
            """
    query_params = [voted_question[0]['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def question_vote_down(cursor, voted_question):
    query = """
            UPDATE question
            SET vote_number = vote_number - 1
            WHERE id = %s;
            """
    query_params = [voted_question[0]['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def answer_vote_up(cursor, voted_answer):
    query = """
            UPDATE answer
            SET vote_number = vote_number + 1
            WHERE id = %s;
            """
    query_params = [voted_answer[0]['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def answer_vote_down(cursor, voted_answer):
    query = """
            UPDATE answer
            SET vote_number = vote_number - 1
            WHERE id = %s;
            """
    query_params = [voted_answer[0]['id']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def get_searched_questions(cursor, search_phrase):
    searched_phrase = f"%{search_phrase}%"
    query = """
            SELECT *
            FROM question 
            WHERE title LIKE %s or message LIKE %s;
            """
    query_params = [searched_phrase, searched_phrase]
    cursor.execute(query, query_params)
    return cursor.fetchall()

    
@database_connection.connection_handler    
def add_comment_to_question(cursor, question_id, comment):
    sub_time = str(util.get_real_time((util.get_unix_timestamp())))
    edited = 0
    query = """
            INSERT INTO comment
            (question_id, message, submission_time, edited_count) 
            VALUES
            (%s, %s, %s, %s);
            """
    query_params = [question_id, comment['message'], sub_time, edited]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def add_comment_to_answer(cursor, answer_id, comment):
    sub_time = str(util.get_real_time((util.get_unix_timestamp())))
    edited = 0
    query = """
            INSERT INTO comment
            (answer_id, message, submission_time, edited_count) 
            VALUES
            (%s, %s, %s, %s);
            """
    query_params = [answer_id, comment['message'], sub_time, edited]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def get_comments_for_question(cursor, question_id):
    query = """
            SELECT *
            FROM comment
            WHERE question_id = %s;
            """
    query_params = [question_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def add_tag_to_question(cursor, id_of_question, tag_name):
    query = """
            INSERT INTO question_tag
            (question_id, name) 
            VALUES
            (%s, %s);
            """
    query_params = [id_of_question, tag_name['name']]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def get_question_tag(cursor, id_of_question):
    query = """
            SELECT *
            FROM question_tag
            WHERE question_id = %s;
            """
    query_params = [id_of_question]
    cursor.execute(query, query_params)
    tags = cursor.fetchall()
    added_tags = []
    try:
        for i in range(len(tags)):
            # tags[i]['name'].set(added_tags)
            if tags[i]['name'] not in added_tags:
                added_tags.append(tags[i]['name'])
    except:
        added_tags = None
    return added_tags


@database_connection.connection_handler
def get_searched_answers(cursor, search_phrase):
    searched_phrase = f"%{search_phrase}%"
    query = """
            SELECT *
            FROM answer 
            WHERE message LIKE %s;
            """
    query_params = [searched_phrase]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler  
def get_comments_for_answer(cursor, answer_id):
    query = """
            SELECT comment.id, comment.message, comment.submission_time, comment.answer_id
            FROM answer
            JOIN comment ON answer.id = comment.answer_id
            WHERE answer.question_id=%s;
            """
    query_params = [answer_id]
    cursor.execute(query, query_params)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_id_from_answer(cursor, answer_id):
    query = sql.SQL("SELECT question_id FROM answer WHERE id=%s;")
    query_params = [int(answer_id)]
    cursor.execute(query, query_params)
    return cursor.fetchall()[0]['question_id']


@database_connection.connection_handler
def get_latest_questions(cursor):
    query = """
            SELECT * FROM question
            ORDER BY id DESC LIMIT 5; 
            """
    cursor.execute(query)
    return cursor.fetchall()


@database_connection.connection_handler
def get_question_id_for_answer_comment(cursor, comment_id):
    query = sql.SQL("SELECT answer.question_id"
                    " FROM comment JOIN answer on comment.answer_id = answer.id"
                    " WHERE comment.id=%s;")
    query_params = [int(comment_id)]
    cursor.execute(query, query_params)
    return cursor.fetchall()[0]['question_id']


@database_connection.connection_handler
def get_question_id_for_question_comment(cursor, comment_id):
    query = sql.SQL("SELECT question_id FROM comment WHERE id=%s;")
    query_params = [int(comment_id)]
    cursor.execute(query, query_params)
    return cursor.fetchall()[0]['question_id']


@database_connection.connection_handler
def delete_comment(cursor, comment_id):
    query = sql.SQL("DELETE FROM comment WHERE id=%s;")
    query_params = [int(comment_id)]
    cursor.execute(query, query_params)


@database_connection.connection_handler
def get_comment_by_id(cursor, comment_id):
    query = sql.SQL("SELECT * FROM comment WHERE id=%s;")
    query_params = [int(comment_id)]
    cursor.execute(query, query_params)
    return cursor.fetchall()[0]


@database_connection.connection_handler
def edit_comment(cursor, comment_id, user_input):
    query = sql.SQL("UPDATE comment SET message = %s WHERE id = %s;")
    query_params = [user_input, int(comment_id)]
    cursor.execute(query, query_params)
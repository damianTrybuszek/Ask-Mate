import os
import csv
import util as util

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\answer.csv'


def file_overwrite(iterable, headers, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
        file.write(",".join(headers)+"\n")
        for item in iterable:
            writer.writerow(item)


def get_questions():
    question_list = []
    with open(DATA_FILE_PATH_QUESTIONS) as file:
        reader = csv.DictReader(file)
        for row in reader:
            question_list.append(row)
    return question_list


def get_question_by_id(question_id):
    questions_list = get_questions()
    for question in questions_list:
        if question['id'] == question_id:
            return question
    return None


def get_answer_by_id(answer_id):
    answers_list = get_answers()
    for answer in answers_list:
        if answer['id'] == answer_id:
            return answer
    return None


def get_headers_questions():
    with open(DATA_FILE_PATH_QUESTIONS) as file:
        lines = file.readlines()
        return lines[0].replace("\n", "").split(",")


def get_headers_answers():
    with open(DATA_FILE_PATH_ANSWERS) as file:
        lines = file.readlines()
        return lines[0].replace("\n", "").split(",")


def get_answers():
    answer_list = []
    with open(DATA_FILE_PATH_ANSWERS) as file:
        reader = csv.DictReader(file)
        for row in reader:
            answer_list.append(row)
    return answer_list


def save_answer(question_id, answer):
    data_list = get_answers()
    answer["submission_time"] = str(util.get_unix_timestamp())
    answer['id'] = str(int(get_max_id(data_list)) + 1)
    answer['vote_number'] = "0"
    answer['question_id'] = question_id
    answer['image'] = ""
    with open(DATA_FILE_PATH_ANSWERS, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=get_headers_answers(), delimiter=",")
        writer.writerow(answer)


def overwrite_question(question):
    questions_list = get_questions()
    for i in range(len(questions_list)):
        if questions_list[i]['id'] == question['id']:
            questions_list[i] = question
    headers = get_headers_questions()
    file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)


def delete_answer(answer):
    answers_list = get_answers()
    headers = get_headers_answers()
    for i in range(len(answers_list)):
        if answers_list[i]['id'] == answer['id']:
            answers_list.pop(i)
            break

    file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)


def save_question(new_question_input):
    data_questions = get_questions()
    new_question_input["id"] = str(int(get_max_id(data_questions)) + 1)
    new_question_input["submission_time"] = str(util.get_unix_timestamp())
    new_question_input["view_number"] = "0"
    new_question_input["vote_number"] = "0"
    new_question_input["image"] = ""

    with open(DATA_FILE_PATH_QUESTIONS, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=get_headers_questions(), delimiter=",")
        writer.writerow(new_question_input)


def get_max_id(iterable_of_dicts):
    if len(iterable_of_dicts) <= 0:
        return 1
    max_id = 0
    max_index = 0
    for index, element in enumerate(iterable_of_dicts):
        if int(element['id']) > max_id:
            max_id = int(element['id'])
            max_index = index
    return iterable_of_dicts[max_index]['id']


def delete_question(question):
    questions_list = get_questions()
    headers = get_headers_questions()
    for i in range(len(questions_list)):
        if questions_list[i]['id'] == question['id']:
            questions_list.pop(i)
            break

    file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)


def question_vote_up(question):
    questions_list = get_questions()
    headers = get_headers_questions()
    for element in questions_list:
        if element['id'] == question['id']:
            temp_vote_number = int(element["vote_number"]) + 1
            element["vote_number"] = str(temp_vote_number)
    file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)


def question_vote_down(question):
    questions_list = get_questions()
    headers = get_headers_questions()
    for element in questions_list:
        if element['id'] == question['id']:
            temp_vote_number = int(element["vote_number"]) - 1
            element["vote_number"] = str(temp_vote_number)
    file_overwrite(questions_list, headers, DATA_FILE_PATH_QUESTIONS)


def answer_vote_up(answer):
    answers_list = get_answers()
    headers = get_headers_answers()
    for element in answers_list:
        if element['id'] == answer['id']:
            temp_vote_number = int(element["vote_number"]) + 1
            element["vote_number"] = str(temp_vote_number)
    file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)


def answer_vote_down(answer):
    answers_list = get_answers()
    headers = get_headers_answers()
    for element in answers_list:
        if element['id'] == answer['id']:
            temp_vote_number = int(element["vote_number"]) - 1
            element["vote_number"] = str(temp_vote_number)
    file_overwrite(answers_list, headers, DATA_FILE_PATH_ANSWERS)

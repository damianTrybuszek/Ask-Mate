import os
import csv
import util as util

DATA_FILE_PATH_QUESTIONS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\question.csv'
DATA_FILE_PATH_ANSWERS = os.getenv('DATA_FILE_PATH') if 'DATA_FILE_PATH' in os.environ else 'sample_data\\answer.csv'


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
    answer['id'] = str(len(data_list)+1)
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
    with open(DATA_FILE_PATH_QUESTIONS, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers, delimiter=",")
        file.write(",".join(headers)+"\n")
        for question in questions_list:
            writer.writerow(question)


def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n-1):
            for j in range(n-i-1):
                if numbers[j][0] > numbers[j+1][0]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]


def save_question(new_question_input):
    data_questions = get_questions()
    new_question_input["id"] = str(len(data_questions)+1)
    new_question_input["submission_time"] = str(util.get_unix_timestamp())
    new_question_input["view_number"] = "0"
    new_question_input["vote_number"] = "0"
    new_question_input["image"] = ""

    with open(DATA_FILE_PATH_QUESTIONS, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=get_headers_questions(), delimiter=",")
        writer.writerow(new_question_input)


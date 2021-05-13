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

def get_headers_questions():
    with open(DATA_FILE_PATH_QUESTIONS) as file:
        lines = file.readlines()
        return lines[0].split(",")

def get_headers_answers():
    with open(DATA_FILE_PATH_ANSWERS) as file:
        lines = file.readlines()
        return lines[0].split(",")
    
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
    with open(DATA_FILE_PATH_ANSWERS, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=get_headers_answers(), delimiter=",")
        writer.writerow(answer)

def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n-1):
            for j in range(n-i-1):
                if numbers[j][0] > numbers[j+1][0]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]

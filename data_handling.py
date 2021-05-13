import os
import csv

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

def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n-1):
            for j in range(n-i-1):
                if numbers[j][0] > numbers[j+1][0]:
                    numbers[j], numbers[j+1] = numbers[j+1], numbers[j]





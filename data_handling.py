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

def get_headers():
    with open(DATA_FILE_PATH) as file:
        lines = file.readlines()
        return lines[0].split(",")
    
def get_answers():
    answer_list = []
    with open(DATA_FILE_PATH_ANSWERS) as file:
        reader = csv.DictReader(file)
        for row in reader:
            question_list.append(row)
    return question_list





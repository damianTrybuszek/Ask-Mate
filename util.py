import time
import data_handling as data_handling


def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)


def sort_table(header, direction, questions_list):
    if header == None or direction == None:
        return questions_list

    headers = []
    new_questions_list = []

    for element in questions_list:
        headers.append(element[header])

    if direction == "asc":
        headers = sorted(headers)[::-1]
    else:
        headers = sorted(headers)

    for i in range(len(headers)):
        searched_header = headers[i]
        for question in questions_list:
            if searched_header == question[header]:
                new_questions_list.append(question)
    return new_questions_list


def edit_single_question(question, new_data):
    for key in new_data:
        question[key] = new_data[key]

def question_vote_up(question):
    temp_vote_number = int(question["vote_number"]) + 1
    question["vote_number"] = str(temp_vote_number)

def question_vote_down(question):
    temp_vote_number = int(question["vote_number"]) - 1
    question["vote_number"] = str(temp_vote_number)

def get_questions_to_display(question_id):
    question_list = data_handling.get_questions()
    if question_id:
        question_to_display = "0"
        for question in question_list:
            if question["id"] == question_id:
                question_to_display = question
        headers = data_handling.get_headers_questions()
    return question_to_display, headers

def get_answer_to_display(question_id):
    answers_to_questions = []
    answer_list = data_handling.get_answers()
    if question_id != 0:
        final_answer_list = []
        for answer in answer_list:
            if answer["question_id"] == question_id:
                # temp_list = [answer["vote_number"], answer["message"], answer['id']]
                answers_to_questions.append(answer)

        if len(answers_to_questions) > 0:
            temp_order_list = []
            for answer in answers_to_questions:
                temp_order_list.append(int(answer['vote_number']))
            bubble_sort(temp_order_list)
            for votes in temp_order_list:
                for answer in answers_to_questions:
                    if answer['vote_number'] == str(votes):
                        final_answer_list.append(answer)
    return final_answer_list

def bubble_sort(numbers):
    n = len(numbers)
    for i in range(n-1):
        for j in range(n-i-1):
            if numbers[j] < numbers[j+1]:
                numbers[j], numbers[j+1] = numbers[j+1], numbers[j]
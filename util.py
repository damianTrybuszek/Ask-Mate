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

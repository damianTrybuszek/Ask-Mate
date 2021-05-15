import time
import data_handling as data_handling


def get_unix_timestamp():
    time_stamp = time.time()
    return int(time_stamp)


def direction_change():
    if direction == "asc":
         direction = "desc"
    else:
        direction = "asc"
    return direction


def sort_table(header, direction, questions_list):
    headers = []
    new_questions_list = []

    for element in questions_list:
        headers.append(element[header])

    if direction == "asc":
        headers = sorted(headers)
    else:
        headers = sorted(headers)[::-1]

    while len(headers) > 0:
        searched_header = headers[0]
        for i in range(len(questions_list)):
            if searched_header == questions_list[i][header]:
                new_questions_list.append(questions_list[i])
                questions_list.pop(i)

    direction_change()
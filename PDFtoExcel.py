
from PyPDF2 import PdfReader
import re
from matplotlib.pyplot import flag
import pandas as pd

pdf_path = r"C:\Users\Fatima\Downloads\PDF example.PDF"


def read_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    number_of_pages = len(reader.pages)
    text = ""
    for i in range(number_of_pages):

        page = reader.pages[i]
        text += page.extract_text()
    return text

# ***************************************************


def extract_quesID(text):

    # pattern = "Question No:\s?\d* "
    pattern = r"Question No:\s?\d*"
    l = re.findall(pattern, text)
    qes_no_list = []
    for token in l:
        qes_no_list.extend(re.findall(r'\d+', token))

    return qes_no_list


def extract_ques_and_answers(text):

    pattern = r"Question No:\s*\d*"
    ques_ans_list = re.split(pattern, text)

    return ques_ans_list[1:]

# --------------------------------------------------


def extract_qes(text):
    print("Inside extract_qes method ")

    my_text = text
    qes_start_pattern = r"Question No:\s*\d*"
    qes_end_pattern = r"A. "

    all_ques = []
    flag = True
    while flag:
        qes_start_match_obj = re.search(qes_start_pattern, my_text)
        qes_end_match_obj = re.search(qes_end_pattern, my_text)

        if qes_start_match_obj != None:
            all_ques.append(my_text[qes_start_match_obj.end(
            ): qes_end_match_obj.start()].replace('\n', " ").strip())
            my_text = my_text[qes_end_match_obj.end():]
        else:
            flag = False

    return all_ques

# --------------------------------------------------


# -------------------------------------------------

def extract_correct_ans(text):
    pattern = r"Answer: [ABCD]"
    all_ans = re.findall(pattern, text)

    return [ans[-1] for ans in all_ans]

# -------------------------------------------------

# *********************************************


def extract_paragraph(text, start_paragraph_pattern, end_paragraph_pattern):

    my_text = text

    all_data = []
    flag = True
    while flag:
        start_match_obj = re.search(start_paragraph_pattern, my_text)
        end_match_obj = re.search(end_paragraph_pattern, my_text)

        if end_match_obj != None:
            all_data.append(
                my_text[start_match_obj.end(): end_match_obj.start()].replace('\n', " ").strip())
            my_text = my_text[end_match_obj.end():]
        else:
            # all_data.append(
            #     my_text[start_match_obj.end():].replace('\n', " ").strip())
            flag = False

    return all_data


# ***********************************************
def extract_explainations(text):

    exp_pattern = r"Explanation: "
    ques_pattern = r"Question No: "

    return extract_paragraph(text, exp_pattern, ques_pattern)

# ***********************************************


# def extract_qes(text):
#     print("Inside extract_qes method ")

#     qes_start_pattern = r"Question No:\s*\d*"
#     qes_end_pattern = r"\w*\?"
#     return extract_paragraph(text, qes_start_pattern, qes_end_pattern)

# *********************************************


def extract_optionA(text):

    start_optionA_pattern = r"A. \w+\."
    return re.findall(start_optionA_pattern, text)
    # return extract_paragraph(text, start_optionA_pattern, end_optionA_pattern)

# *********************************************


def to_csv(ques_no, ques, ans, exp, file_name=r'Output8.csv'):

    file = open(file_name, "a")
    file.write("Question ID, Answer, Explanation")

    for qid, q, ans, ex in zip(ques_no, ques, ans, exp):
        file.write("\n" + qid + "," + q + "," + ans + "," + ex)

    file.close()


if __name__ == "__main__":

    text = read_pdf(pdf_path)

    ques_no = extract_quesID(text)

    ques = extract_qes(text)

    ans = extract_correct_ans(text)

    exp = extract_explainations(text)

    optionA = extract_optionA(text)
    # to_csv(ques_no, ques, ans, exp)
    # print(type(optionA))
    for i in optionA:

        print(i)
        print("***********")

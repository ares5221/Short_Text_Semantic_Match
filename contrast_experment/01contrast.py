#!/usr/bin/env python
# _*_ coding:utf-8 _*_、
import csv

import xlwt
from bert_serving.client import BertClient
from utils.consine_similarity import cal_cosine


def get_csv_data(filename):
    ques_data = []
    with open(filename, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            ques_data.append(row)
    print('get data size',len(ques_data))
    return ques_data



def test_no_similarly_sentences_pairs():
    bc = BertClient()
    sim_Threshold = 0.5  # 认为不相似的阈值设定
    no_similarly_sentences_file_name = './../data/no_similarly_sentences_pairs.csv'
    no_similarly_sentences_data = get_csv_data(no_similarly_sentences_file_name)

    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True)  # sheet1保存不相似问句及相似度
    sheet2 = book.add_sheet(u'Sheet2', cell_overwrite_ok=True)  # sheet2保存相似问句及相似度

    for index in range(len(no_similarly_sentences_data)):
        sentences_pair = no_similarly_sentences_data[index]
        print(sentences_pair)
        sentences_1 = sentences_pair[0]
        sentences_2 = sentences_pair[1]
        word_vec1 = bc.encode([sentences_1])
        word_vec2 = bc.encode([sentences_2])
        sim_val = cal_cosine(word_vec1[0], word_vec2[0])
        print(index, ' ', sim_val)
        if sim_val < sim_Threshold:
            sim_text = [index, sentences_1, sentences_2, sim_val]
            for cols in range(4):
                sheet1.write(index, cols, sim_text[cols])
        else:
            sim_text = [index, sentences_1, sentences_2, sim_val]
            for cols in range(4):
                sheet2.write(index, cols, sim_text[cols])

        sim_file_name = 'no_similarly_setntence_val' + '.xls'
        book.save(sim_file_name)




def test_similarly_sentences_pairs():
    bc = BertClient()
    sim_Threshold = 0.7 # 认为相似的阈值设定
    similarly_sentences_file_name = './../data/similarly_sentences_pairs.csv'
    similarly_sentences_data = get_csv_data(similarly_sentences_file_name)

    book = xlwt.Workbook(encoding='utf-8')  # 创建Workbook，相当于创建Excel
    sheet1 = book.add_sheet(u'Sheet1', cell_overwrite_ok=True) #sheet1保存相似问句及相似度
    sheet2 = book.add_sheet(u'Sheet2', cell_overwrite_ok=True) #sheet2保存不相似问句及相似度

    for index in range(len(similarly_sentences_data)):
        sentences_pair = similarly_sentences_data[index]
        sentences_1 = sentences_pair[0]
        sentences_2 = sentences_pair[1]
        word_vec1 = bc.encode([sentences_1])
        word_vec2 = bc.encode([sentences_2])
        sim_val = cal_cosine(word_vec1[0], word_vec2[0])
        print(index, ' ', sim_val)
        if sim_val > sim_Threshold:
            sim_text = [index, sentences_1, sentences_2, sim_val]
            for cols in range(4):
                sheet1.write(index, cols, sim_text[cols])
        else:
            sim_text = [index, sentences_1, sentences_2, sim_val]
            for cols in range(4):
                sheet2.write(index, cols, sim_text[cols])

        sim_file_name = 'similarly_setntence_val' + '.xls'
        book.save(sim_file_name)


if __name__ == '__main__':
    # test_similarly_sentences_pairs()
    test_no_similarly_sentences_pairs()
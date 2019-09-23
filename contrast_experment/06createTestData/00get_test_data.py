#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import csv
from bert_serving.client import BertClient
import os
import numpy as np
import pkuseg
import json
'''
将100对测试句子放到同一个文件中，添加标签
然后生成对应的数据格式 npy
'''
root_dir = os.path.abspath('./../../data/')
print(root_dir)
def read_data():
    same_sen_file_name = root_dir + 'similarly_sentences_pairs.csv'
    no_same_sen_file_name = root_dir + 'no_similarly_sentences_pairs.csv'
    same_sens = []
    no_same_sens = []

    with open(same_sen_file_name, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            same_sens.append(row)
    with open(no_same_sen_file_name, 'r', encoding='utf-8') as fcsv1:
        csv_reader1 = csv.reader(fcsv1)  # 使用csv.reader读取csvfile中的文件
        for row1 in csv_reader1:
            no_same_sens.append(row1)
    print(len(same_sens), len(no_same_sens))
    return same_sens, no_same_sens


def save_sens_csv(same_sens, no_same_sens):
    test_data = []
    with open('test_sentences_pairs_100.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ')
        for same_sen in same_sens:
            # print(type(same_sen[0]))
            test_data.append([same_sen[0] + ',' + same_sen[1] + ',' + '1'])
            spamwriter.writerow([same_sen[0] + ',' + same_sen[1] + ',' + '1'])
        for no_same_sen in no_same_sens:
            # print(no_same_sens[0])
            test_data.append([no_same_sen[0] + ',' + no_same_sen[1] + ',' + '0'])
            spamwriter.writerow([no_same_sen[0] + ',' + no_same_sen[1] + ',' + '0'])
    return test_data


def encode_test_data1(data):
    '''
    为bert lstm pooling mlp造的100条测试数据
    :param data:
    :return: test_data1.npy test_data2.npy test_label.npy
    '''
    test_label = []  # 用于存储每对句子的是否相似的标签信息1，0
    sentences1_seg_list = [[] for index in range(len(data))]  # 存储第一个句子和第二个句子的分词结果
    sentences2_seg_list = [[] for index in range(len(data))]
    word_index_dic = {}
    qinghuaSeg = pkuseg.pkuseg()
    for i in range(len(data)):
        sen1 = data[i][0].split(',')[0]
        sen2 = data[i][0].split(',')[1]
        test_label.append(int(data[i][0].split(',')[2]))
        seg_content_data1 = qinghuaSeg.cut(sen1)
        seg_content_data2 = qinghuaSeg.cut(sen2)
        # 将分词结果保存到对应数组
        sentences1_seg_list[i] = seg_content_data1
        sentences2_seg_list[i] = seg_content_data2
        # print('已经完成进度', i / 100)

    # save label info
    if not os.path.exists("test_label.npy"):
        np.save("test_label.npy", np.array(test_label))
    with open('word_index_dict.json', 'r', encoding='utf-8') as f:
        word_index_dic = json.load(f)
    sentences1_data = []
    sentences2_data = []
    for ssl1 in range(len(sentences1_seg_list)):
        word_vec_list1 = []
        for word in sentences1_seg_list[ssl1]:
            if word in word_index_dic:
                word_vec_list1.append(word_index_dic[word])
            else:
                word_vec_list1.append(0)
        sentences1_data.append(word_vec_list1)
    for ssl2 in range(len(sentences2_seg_list)):
        word_vec_list2 = []
        for word in sentences1_seg_list[ssl2]:
            if word in word_index_dic:
                word_vec_list2.append(word_index_dic[word])
            else:
                word_vec_list2.append(0)
        sentences2_data.append(word_vec_list2)
    if not os.path.exists("test_data1.npy"):
        np.save("test_data1.npy", sentences1_data)
    if not os.path.exists("test_data2.npy"):
        np.save("test_data2.npy", sentences2_data)


def encode_test_data2(data):
    '''
    构造用于bert mlp的测试数据 用于03bert mlp文件夹的数据
    :param data:
    :return:test_data3 test_label3
    '''
    test_label3 = []  # 用于存储每对句子的是否相似的标签信息1，0
    test_data3 = [[] for i in range(len(data))]  # 存储第一个句子和第二个句子的embedding结果
    bc = BertClient()
    for i in range(len(data)):
        sen1 = data[i][0].split(',')[0]
        sen2 = data[i][0].split(',')[1]
        test_label3.append(int(data[i][0].split(',')[2]))
        sen12vec = bc.encode([sen1])
        sen22vec = bc.encode([sen2])
        ss = np.append(sen12vec, sen22vec)
        test_data3[i] = ss.tolist()
    np.save('test_data3.npy', test_data3)
    np.save('test_label3.npy', test_label3)



if __name__ == '__main__':
    same_sens, no_same_sens = read_data()

    test_data = save_sens_csv(same_sens, no_same_sens)
    print('save test sentences with label(0 1) ok', '-'*50)
    if not os.path.exists('test_data1.npy'):
        encode_test_data1(test_data)
        print('save test_data1, test_data2, test_label ok', '-'*50)
    if not os.path.exists('test_data3.npy'):
        encode_test_data2(test_data)
        print('save test_data3, test_label3 ok', '-'*50)
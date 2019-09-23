#!/usr/bin/env python
# _*_ coding:utf-8 _*_
'''
身体攻击行为
言语攻击行为
关系攻击行为
非扰乱性课堂违纪行为
扰乱课堂秩序行为
违反课外纪律行为
欺骗行为
偷盗行为
背德行为
言语型退缩
行为型退缩
心理型退缩
抑郁问题
焦虑问题
学习能力问题
学习方法问题
学习态度问题
注意力问题
自我吹嘘型问题
执拗型问题
自私型问题
沉迷行为
早恋行为
极端行为
'''
import csv
import random



def read_data():
    filename = 'clean_source_data.csv'
    data = [[] for i in range(24)]
    with open(filename, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            if row[0] == 'label11':
                data[0].append(row[1])
            elif row[0] == 'label12':
                data[1].append(row[1])
            elif row[0] == 'label13':
                data[2].append(row[1])
            elif row[0] == 'label14':
                data[3].append(row[1])
            elif row[0] == 'label15':
                data[4].append(row[1])
            elif row[0] == 'label16':
                data[5].append(row[1])
            elif row[0] == 'label17':
                data[6].append(row[1])
            elif row[0] == 'label18':
                data[7].append(row[1])
            elif row[0] == 'label19':
                data[8].append(row[1])
            elif row[0] == 'label20':
                data[9].append(row[1])

            elif row[0] == 'label21':
                data[10].append(row[1])
            elif row[0] == 'label22':
                data[11].append(row[1])
            elif row[0] == 'label23':
                data[12].append(row[1])
            elif row[0] == 'label24':
                data[13].append(row[1])
            elif row[0] == 'label25':
                data[14].append(row[1])
            elif row[0] == 'label26':
                data[15].append(row[1])
            elif row[0] == 'label27':
                data[16].append(row[1])
            elif row[0] == 'label28':
                data[17].append(row[1])
            elif row[0] == 'label29':
                data[18].append(row[1])

            elif row[0] == 'label30':
                data[19].append(row[1])
            elif row[0] == 'label31':
                data[20].append(row[1])
            elif row[0] == 'label32':
                data[21].append(row[1])
            elif row[0] == 'label33':
                data[22].append(row[1])
            elif row[0] == 'label34':
                data[23].append(row[1])

    # for item in data:
    #     print(len(item))
    # for item in data[21]:
    #     print(item)
    return data


def get_sim_sen_pairs(data):
    count = 0
    with open('same_label_sentences_pairs_10w.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ')
        for index in range(120000):
            ran_cla = random.randint(0, len(data) - 1)
            first_sen = random.randint(0, len(data[ran_cla]) - 1)
            second_sen = random.randint(0, len(data[ran_cla]) - 1)
            if first_sen != second_sen:
                count += 1
                if count > 100000:
                    print('ok')
                    break
                if count % 10000 == 0:
                    print([data[ran_cla][first_sen] + ' ' + data[ran_cla][second_sen] + ' ' + '1'])
                spamwriter.writerow([data[ran_cla][first_sen] + ',' + data[ran_cla][second_sen] + ',' + '1'])



def get_no_sim_sen_pairs(data):
    count = 0
    with open('no_same_label_sentences_pairs_10w.csv', 'w', newline='', encoding='utf-8') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ')
        for index in range(120000):
            ran_cla1 = random.randint(0, len(data) - 1)
            ran_cla2 = random.randint(0, len(data) - 1)
            if ran_cla1 != ran_cla2:
                first_sen = random.randint(0, len(data[ran_cla1]) - 1)
                second_sen = random.randint(0, len(data[ran_cla2]) - 1)
                count += 1
                if count > 100000:
                    print('ok')
                    break
                if count % 10000 == 0:
                    print([data[ran_cla1][first_sen] + ' ' + data[ran_cla2][second_sen] + ' ' + '0'])
                spamwriter.writerow([data[ran_cla1][first_sen] + ',' + data[ran_cla2][second_sen] + ',' + '0'])



if __name__ == '__main__':
    data = read_data()
    get_sim_sen_pairs(data)
    print('sim ok------------------------------------------------------------')
    get_no_sim_sen_pairs(data)
    print('diff ok ----------------------------------------------------------')
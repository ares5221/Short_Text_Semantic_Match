#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv

def pre_clean():
    filename = 'ann_source_data.csv'
    count = 0
    with open(filename, 'r', encoding='utf-8') as fcsv:
        csv_reader = csv.reader(fcsv)  # 使用csv.reader读取csvfile中的文件
        for row in csv_reader:
            newss = row[1]
            if ',' in row[1]:
                print(row[1])
                newss = row[1].replace(',','，')
                count +=1
            newrow = [row[0],newss]
            with open("clean_source_data.csv", "a", encoding='utf-8',newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(newrow)

        print('修改',count)

if __name__ == '__main__':
    pre_clean() # 将标注数据中的英文都好改为中文逗号，否则对后面的有影响
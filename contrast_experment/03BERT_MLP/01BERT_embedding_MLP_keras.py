#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv
import os
import pandas as pd
import jieba
import numpy as np
import json
import tensorflow as tf
from tensorflow import keras
import matplotlib.pyplot as plt
from bert_serving.client import BertClient
from keras.utils import np_utils



# 通过bert将句子embedding
def peredata(content_data):
    print('step2: 通过BERT将句子embedding转换成向量...')
    data = content_data.tolist()
    train_label = []  # 用于存储每对句子的是否相似的标签信息1，0
    train_data = [[] for i in range(len(data))]  # 存储第一个句子和第二个句子的embedding结果
    bc = BertClient()
    for i in range(len(data)):
        sen1 = data[i][0].split(',')[0]
        sen2 = data[i][0].split(',')[1]
        train_label.append(int(data[i][0].split(',')[2]))
        sen12vec = bc.encode([sen1])
        sen22vec = bc.encode([sen2])
        ss = np.append(sen12vec, sen22vec)
        train_data[i] = ss.tolist()
        if i % 1000 == 0:
            print('已经完成进度', i/200000)
    np.save('train_data.npy', train_data)
    np.save('train_label.npy', train_label)
    print('step2: BERT转换向量完成，success')
    return train_data, train_label


def build_model(train_data, train_label, test_data, test_label):
    print('step3: start build MLP model...')
    data_size = 200000
    max_len = 768*2  # BERT Embedding length
    epochs_num = 400
    batch_size_num = 100
    #set train data
    train_data = keras.preprocessing.sequence.pad_sequences(train_data,
                                                            padding='post',
                                                            maxlen=max_len)
    train_label = np.array(train_label)
    train_label = np_utils.to_categorical(train_label, 2)
    # set test data
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,
                                                            padding='post',
                                                            maxlen=max_len)
    test_label = np.array(test_label)
    test_label = np_utils.to_categorical(test_label, 2)

    model = keras.Sequential()
    model.add(keras.layers.Dense(100, activation=tf.nn.sigmoid, input_shape=(768*2,)))
    model.add(keras.layers.Dense(2, activation=tf.nn.sigmoid))
    model.summary()
    # 损失函数和优化
    model.compile(optimizer=tf.train.AdamOptimizer(),
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    train_test_split_num = int(data_size * 0.8)
    train_val_split_num = int(train_test_split_num * 0.8)
    x_val = train_data[train_val_split_num:train_test_split_num]
    partial_x_train = train_data[0:train_val_split_num]
    y_val = train_label[train_val_split_num:train_test_split_num]
    partial_y_train = train_label[0:train_val_split_num]
    #使用20w构造数据中的一部分4w数据作为test数据
    test_data = train_data[train_test_split_num:]
    test_labels = train_label[train_test_split_num:]
    # 使用人工构造的论坛问答数据中的100条数据作为test数据 理论上效果会比val_acc差
    # test_data = test_data
    # test_labels = test_label

    history = model.fit(partial_x_train,
                        partial_y_train,
                        epochs=epochs_num,
                        batch_size=batch_size_num,
                        validation_data=(x_val, y_val),
                        shuffle=True
                        )

    results = model.evaluate(test_data, test_labels)
    print('step5: 评估模型效果(损失-精度）：...', results)

    print('step6: predict test data for count...')
    # predictions = model.predict(test_data, batch_size=batch_size_num)
    # predict = np.argmax(predictions, axis=1)
    predictions = model.predict_classes(test_data)
    print(predictions)
    with open('03bert_lstm_mlp_predict_keras.csv', 'w', newline='', encoding='utf-8') as csvwriter:
        spamwriter = csv.writer(csvwriter, delimiter=' ')
        for pre_val in predictions:
            spamwriter.writerow([pre_val])

    count = 0
    for res in range(len(predictions)):
        if res < 50:
            if predictions[res] == 1:
                count += 1
        else:
            if predictions[res] == 0:
                count += 1
    print(count)
    # print('step6: 开始绘图...')
    # history_dict = history.history
    # history_dict.keys()
    # acc = history.history['acc']
    # val_acc = history.history['val_acc']
    # loss = history.history['loss']
    # val_loss = history.history['val_loss']
    # epochs = range(1, len(acc) + 1)
    # # "bo" is for "blue dot"
    # plt.plot(epochs, loss, 'bo', label='Training loss')
    # # b is for "solid blue line"
    # plt.plot(epochs, val_loss, 'b', label='Validation loss')
    # plt.title('Training and validation loss')
    # plt.xlabel('Epochs')
    # plt.ylabel('Loss')
    # plt.legend()
    # plt.show()
    # plt.clf()  # clear figure
    # plt.plot(epochs, acc, 'bo', label='Training acc')
    # plt.plot(epochs, val_acc, 'r', label='Validation acc')
    # plt.title('Training and validation accuracy')
    # plt.xlabel('Epochs')
    # plt.ylabel('Accuracy')
    # plt.legend()
    # plt.show()
    print('模型训练结束！！！！！')


# setp 0
def execute():
    # step 1 load source data 20w
    if os.path.exists('data.npy'):
        data_list = np.load("data.npy",allow_pickle=True)
    else:
        print('读取生成的20w条标记数据作为训练分类的训练数据')
    # step 2.1 load bert embedding train data/label
    if os.path.exists('train_data.npy') and os.path.exists('train_label.npy'):
        train_data = np.load("train_data.npy",allow_pickle=True)
        train_label = np.load("train_label.npy",allow_pickle=True)
    else:
        train_data, train_label = peredata(data_list)

    # step 2.2 load bert embedding test data/label
    if os.path.exists('test_data3.npy') and os.path.exists('test_label3.npy'):
        test_data = np.load("test_data3.npy", allow_pickle=True)
        test_label = np.load("test_label3.npy", allow_pickle=True)
    else:
        pass
    # step 3 train MLP model
    build_model(train_data, train_label, test_data, test_label)


# START
if __name__ == '__main__':
    print('通过BERT做embedding的部分，将句子转换为768长度的向量,后接keras实现的MLP分类')
    execute()

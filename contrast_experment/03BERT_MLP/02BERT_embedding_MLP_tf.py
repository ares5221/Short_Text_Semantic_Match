#!/usr/bin/env python
# _*_ coding:utf-8 _*_
import csv

import tensorflow as tf
import numpy as np
from keras.utils import np_utils

'''
训练标注文本分类的MLP模型 X_data Y_data为label_text.csv通过bert embedding后的结果及对应标签
2824条标注数据 2019/6/11 updata   Accuracy: 0.25925925
'''

X = np.load('train_data.npy')
Y = np.load('train_label.npy')
test_data = np.load("test_data3.npy", allow_pickle=True)
test_label = np.load("test_label3.npy", allow_pickle=True)

print('导入train数据成功', X.shape, Y.shape)
print('导入test数据成功', test_data.shape, test_label.shape)

Y_label = np_utils.to_categorical(Y, 2)
t_lable = np_utils.to_categorical(test_label,2)
## use self test data 4w
X_train, X_test = X[0:160000], X[160000:]
Y_train, Y_test = Y_label[0:160000], Y_label[160000:]
## use qa test data 100
# X_train, X_test = X[0:160000], test_data
# Y_train, Y_test = Y_label[0:160000], t_lable

tf.reset_default_graph()
# Parameters
learning_rate = 0.001
training_epochs = 200
batch_size = 100
display_step = 10

# Network Parameters
n_input = 768*2  # Number of feature
n_hidden_1 = 100  # 1st layer number of features
n_classes = 2  # Number of classes to predict

x = tf.placeholder("float", [None, n_input])
y = tf.placeholder("float", [None, n_classes])


# Create model
def multilayer_perceptron(x, weights, biases):
    layer_1 = tf.add(tf.matmul(x, weights['h1']), biases['b1'])
    layer_1 = tf.nn.sigmoid(layer_1)
    out_layer = tf.matmul(layer_1, weights['out']) + biases['out']
    out_layer = tf.nn.softmax(out_layer)
    return out_layer


# Store layers weight & bias
weights = {
    'h1': tf.Variable(tf.random_normal([n_input, n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_hidden_1, n_classes]))
}
biases = {
    'b1': tf.Variable(tf.random_normal([n_hidden_1])),
    'out': tf.Variable(tf.random_normal([n_classes]))
}

# Construct model
pred = multilayer_perceptron(x, weights, biases)

# Define loss and optimizer
cost = tf.reduce_mean(tf.nn.sigmoid_cross_entropy_with_logits(logits=pred, labels=y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)

# Initializing the variables
init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)

    saver = tf.train.Saver(max_to_keep=4)  # save model
    for epoch in range(training_epochs):  # Training cycle
        avg_cost = 0.
        total_batch = int(len(X_train) / batch_size)
        X_batches = np.array_split(X_train, total_batch)
        Y_batches = np.array_split(Y_train, total_batch)
        for i in range(total_batch):  # Loop over all batches
            batch_x, batch_y = X_batches[i], Y_batches[i]
            # Run optimization op (backprop) and cost op (to get loss value)
            _, c = sess.run([optimizer, cost], feed_dict={x: batch_x,
                                                          y: batch_y})
            avg_cost += c / total_batch  # Compute average loss
        saver.save(sess, 'ckptann/mlp.ckpt', global_step=epoch)
        if epoch % display_step == 0:  # Display logs per epoch step
            print("Epoch:", '%04d' % (epoch + 1), "cost=", "{:.9f}".format(avg_cost))
    print("Optimization Finished!")

    # Test model
    correct_prediction = tf.equal(tf.argmax(pred, 1), tf.argmax(y, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
    print("Accuracy:", accuracy.eval({x: X_test, y: Y_test}))  # Accuracy: 0.9905
    # global result
    result = tf.argmax(pred, 1).eval({x: X_test, y: Y_test})
    print(result)
    with open('03bert_lstm_mlp_predict_tf.csv', 'w', newline='', encoding='utf-8') as csvwriter:
        spamwriter = csv.writer(csvwriter, delimiter=' ')
        for pre_val in result:
            spamwriter.writerow([pre_val])
    count =0
    for res in range(len(result)):
        if res <50:
            if result[res] ==1:
                count+=1
        else:
            if result[res] ==0:
                count +=1
    print(count)
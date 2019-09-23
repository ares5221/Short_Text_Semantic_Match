##本文件夹代码用于对比实验部分

###验证模型有效性bert+consina
手动构建论文问答数据的相似问题数据集50个问题对./../data/similarly_sentences_pairs.csv及不相似问题数据集50个问题对no_similarly_sentences_pairs.csv

01contrast.py中比较通过bert word embedding然后仅仅使用consina计算向量相似度，从而推断
是否为相似问题，依次在两个构建的数据集上做验证

得到的结果保存在no_similarly_setntence_val.xls similarly_setntence_val.xls


###验证模型有效性bert+lstm+pooling+mlp
02BERT_LSTM_Pooling_MLP文件夹中通过构建模型做问题对相似度比较
具体实现思路见其中00readme.md


###验证模型有效性bert+mlp
03BERT_MLP文件夹中通过构建模型做问题对相似度比较
01BERT_embedding_MLP_keras.py将20w问题对Moral数据BERT转换为向量后拼接为768*2长度的向量，然后通过keras的dense层做mlp分类
02BERT_embedding_MLP_tf.py将20w问题对数据BERT转换为向量后拼接为768*2长度的向量，然后通过tf源码修改做mlp分类，数据需要来源于上面生成的train_data train_label


###验证模型有效性bert+lstm+pooling+mlp在LCQCM数据集上的结果
04BERT_LSTM_Pooling_MLP_with_LQCMC文件夹中通过构建模型对LCQMC数据集做问题对相似度比较
数据集位于.\QAinBERT\QAsrc\data\LCQMC


###验证模型有效性bert+mlp在LCQCM数据集上的结果
05BERT_LSTM_Pooling_MLP_with_LQCMC文件夹中通过构建模型对LCQMC数据集做问题对相似度比较
数据集位于.\QAinBERT\QAsrc\data\LCQMC


###构造测试数据100对，在使用的时候直接替换进去即可
06createTestData
将人工生成的论坛问答对的100对数据作为模型的测试数据
先保存在test_sentences_pairs_100.csv 并给打上标签 1代表语义相同，0表示语义不同

生成的test_data1.npy test_data2.npy test_label.npy是用于bert+lstm+polling+mlp模型的数据
可以用于02 04实验，使用的时候直接导入，参数传递进去，然后作为test_data即可

生成的test_data3.npy test_label3.npy是用于bert+mlp模型，可以用于03 05实验
使用的时候直接导入，参数传递进去，然后作为test_data即可


###根据模型预测结果来统计如果加入topic info信息是否可以提高准确率
07countTopicInfo
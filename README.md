# Short_Text_Semantic_Match

本项目用于实现短文本语义匹配的实现。

##项目背景：

实际场景需求为问答系统中，需要根据用户的输入query找到问答数据库中最相似的问题语句，进而将其答案返回给用户。

这里涉及到比较语句之间的语义相似度，进而排序的过程。也就是短文本语义匹配的问题。

由于当前已经有基于上下文语义理解的预训练模型，我们优先尝试的是基于BERT + cosina的方式。实际工程中由于会结合排序，因此效果还可以，对结果也可以解释。但是这里有个前提是问答数据是多领域的时候效果较好，由于BERT，Elmo等pre-train模型是基于多领域来训练的，当任务属于domain的单领域时候，对于本身语义区分度不大的语句，要做语义匹配或者分类就达不到期望的结果。

这个项目会依次尝试不同的文本语义匹配方式，并比较其效果。


Bert情感分析   
算法描述：  ①使用Wiki语料预训练模型，减少训练时间，分割训练集和测试集。  
           ②建立词典与每个词对索引的映射，添加特殊Token，如CLS\SEP\PAD\UKN等。  
                                 ③建立DataSet与Dataloader。  
                                 ④记下当前epoch的AUC，如果当前的AUC较上一个epoch没有提升，那就降低学习率，采取early stop对十回合AUC没有发生变化就终止。  
                                 ⑤使用mean_max_pooling方法对attention矩阵进行处理，防止过拟合，提高准确率。  
                                 ⑥将得到的Attention矩阵进行画图可视化。  
AUC of train/test  
![image](https://user-images.githubusercontent.com/78432083/109452111-f8e81680-7a89-11eb-8fbc-5ad713e8b52f.png)   
解决过拟合，使用mean_max pooling  
![image](https://user-images.githubusercontent.com/78432083/109452511-d4d90500-7a8a-11eb-9198-e86cbd94700b.png)  
生成的注意力矩阵如下：（其中每一行代表每个字在句子中的重要程度）  
![image](https://user-images.githubusercontent.com/78432083/109452651-34cfab80-7a8b-11eb-8768-4b7fee117a5d.png)  

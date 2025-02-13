## Introduction
- Journal: *Nature Machine Intelligence* 
- Textbook: 周志华《机器学习》
- sklearn-user guide
- pytorch/scipy的documentation
- http://cfff.fudan.edu.cn/home 校园网访问
- https://university.aliyun.com 互联网访问 学生免费算力支持
> Big data is defined as a collection of data which is unfeasible to processed, searched or analyzed by hand database tools due to its large size and complexity
- 机器学习：搞出未知的函数关系；分类聚类回归降维
    - 监督：tags given
    - 无监督：no tags
    - 强化：awards approach
    - 深度学习：CCN，RNN，LSTM

## AI_for_CHEM-关键概念
- 描述化学体系
    - 描述符
    - 降维/精细-粗粝
    - 分子动力学：可基于键长角、电荷，或基于周围环境
    - 结构-性质问题：图or基于图的压缩线性字符串（SMILES）/分子指纹
- 监督学习
    - Loss Function==MSE；交叉熵
    - **过拟合**or欠拟合
    - 正则化：增加对参数复杂度的惩罚项，L2时称为**脊函数**
    - 边际似然：贝叶斯统计
    - 交叉验证
    - Early stop：迭代法中防治过拟合
- 非监督学习
    - 降维，聚类
- 强化学习
    - 决策，通过奖励-惩罚
## AI_for_CHEM-常见方法
- 监督-线性回归
    $$\hat{y}=\omega^{T}x+b$$
    - 其中待优化参数是w和b，L2损失函数，则可解析求解
    - 广义线性回归
- 监督-非线性回归
    - 若模型已知，亦可进行拟合
    - 一般无法解析
    - 易造成过拟合
    - 最近邻模型-k
        - 推广：核函数
    - 核函数：度量两点**相似程度**的函数
        - Gaussian Kernel
        - Rational Quadratic Kernel
        - Periodic Kernel
        - Sigmoid Kernel
        - 超参
    - 核脊回归
        $$\hat{y}=\omega^{T}\mathbb{k}+b$$
        - 根据估计点和全部点的相似度得到k去做回归
        - Kernel矩阵/协方差矩阵
        - GPR基于贝叶斯统计
        - 超参也需要优化，grid search，亦可基于MLE优化
        - GPR可以学习高阶导数数据，加入导数信息通常很有效
        - 训练：o(M3)，预测：o(M)，存储：o(M2)，用于$10^{12}$以下的小样本学习
- 监督-逻辑回归 Logistic Regression
    - 主要用于二元分类，根据给定自变量x预测属于该类的概率，即得到(x , Prob of class)
    $$\hat{p}(x)=\frac{1}{1+e^{-w^Tx-b}}$$
    - 亦可用于非线性回归
- 监督-支持向量机(SVM)
    - 线性分类：在d维参数空间寻找d-1维的超平面
    - 硬边界：使得被分划分的两边距离最大？
    - 软边界：增加一个惩罚函数
- 监督-决策树(Decision Tree)
    - 模仿人类“分情况讨论”的模型
    - 难以优化
    - 改进：随机森林(Random Forest)
- 非监督-主成份分析(PCA)
    - 维度缩减的方法
    $$M=U\Sigma V^T$$
    - U and V are orthogonal
- 非监督-非线性维度缩减
    - 复杂的高维表示空间使用PCA效果不佳
    - 可通过核函数改造
    - MDS：将高维空间上的点映射到低维，但尽量保证点之间的距离不变
- 非监督-分级聚类法
    - **凝聚**：自下而上，逐一合并*距离相近*者
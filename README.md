# statiip-platform
statiip platform project


## 项目目录
```
GUI                        
├── data			    # 基本实验数据
│   ├── hw1				    # hw1数据
│   ├── hw2				    # hw2数据
│   ├── hw3				    # hw3数据
│   └── hw4                  # hw4数据
├── static              # flask框架静态文件
│   ├── data    			
│   ├── dist                   	
│   ├── js     			
│   ├── less    	
│   ├── ……		
│   └── vendor             
├── templates           # 动态网页模板
│   ├── hw1.html            # hw1网页		
│   ├── hw2.html            # hw2网页
│   ├── hw3_share.html      # hw3股票预测网页	
│   ├── hw3_token.html	    # hw3中文分词网页
│   ├── hw4.html    	    # hw4网页	
│   ├── introduction.html   # 介绍网页 		
│   └── layout.html         # 模板网页
├── back.py             # flask app脚本
├── hw1.py              # hw1脚本
├── hw1_extra.py        # hw1大数据集的脚本
├── hw2.py              # hw2脚本
├── hw3_token.py        # hw3中文分词脚本
├── hw3_share.py        # hw3股票预测脚本
├── hw4.py        	    # hw4脚本
└── 说明文档20170106.pdf # 说明文档
```



## 使用环境
1. 系统环境：win python 2.7

2. 依赖包：flask,chartkick,pycrfsuite

   ​


## 使用说明

-   在工作目录下运行back.py脚本

-   打开对应的http://localhost:5000网页

-   introduction页面中介绍了所有homework的要求和预计完成时间，右上角可以查看每个homework的完成状况
    - homework1和homework2全部完成
    - homework3全部完成
    - homework4全部完成

-   左侧导航栏跳转到具体homework界面





## 详细说明
### homework1

部分在线训练，部分导入数据

- 小数据集训练：在后台进行实时训练
  - 开始训练：如果测试结果出错，将显示出错邮件内容
  - 循环100次：显示循环100次之后的错误率
- CSDMC2010_SPAM数据集：导入预先数据
  - 训练结果：显示TF_IDF，Error rate，F rate折线图，测试结果和最终的分类结果（部分）

### homework2

导入预先数据

- 训练结果
  - 显示20ng和webkb数据集，有无标签数据和没有之间的对比折线图
  - 显示r8，r52数据集，两种方法之间的对比表格

### homework3
- 中文分词：部分导入数据，部分在线训练
  - 性能结果呈现表格形式
- 股票预测：导入预先数据和图片
  - 散点图因为数据过大在网页上绘制不方便，暂时采用引入预先matplotlib绘制的图片

### homework4

部分导入数据，部分在线训练

- 分词性能
  - 性能呈现表格形式
  - 导入预先处理好的结果

- 新词发现

  - 在线分词，对分词结果进行新词检验

- 错词取样

  - 显示开发集中错误分词的句子
  - 每次点击“错词取样”将会随机出现不同的错句

- HMM和CRF性能对比
  - 分词对比使用预先训练好的参数在线分词，测试文本可改变

    ​


## 注意事项
1.   网页在初始状态下，只显示为测试结果预留的空白部分，只有点击相应的按钮，后台python才会进行相应的训练和测试
2.   由于部分数据训练和测试时间较长，网页加载过慢，因此运行时间超过1分钟的数据，均事先运行好，将结果保存在data文件夹中，网页显示时只导入预先数据




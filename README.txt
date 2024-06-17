文件说明：
        1.test文件夹：用于存放用来测试的数据
        2.label_data文件夹：用于存放自己标注的数据
        3.运行截图文件夹：用于存放运行截图的信息
        4.img文件夹：可以存放供前端测试的任意图片
        5.output文件夹：存放在前端识别后的图片
        6.predict.py：用于测试数据
        7.frontend文件夹：存放前端的相关内容
        8.util文件夹：存放模型加载、绘图以及测试数据的相关代码
        9.nets文件夹：存放训练用的网络的相关内容
       10.yolo.py：涉及目标检测、数据测试的内容
       11.detection.py：由app.py调用的脚本，用于识别图片
       12.app.py：Flask应用的入口文件。
       13.logs文件夹：存放由我们小组训练好的权重文件（270mb左右）

运行说明：
        1.直接运行predict.py，terminal窗口做出 metric 的输出
        2.terminal的输出格式为”Map = class AP    || score_threhold= x : F1= x ; Recall= x ; Precision= x“ 其中， score_threhold 代表IoU, mean average precision在最左侧，例如：
90.52% = apple AP       ||      score_threhold=0.5 : F1=0.86 ; Recall=91.43% ; Precision=82.05%
94.80% = banana AP      ||      score_threhold=0.5 : F1=0.89 ; Recall=85.00% ; Precision=94.44%
94.53% = orange AP      ||      score_threhold=0.5 : F1=0.92 ; Recall=92.86% ; Precision=90.70%
mAP = 93.29%      ||    All_score_threhold=0.5 : F1=0.89 ; All_Recall=89.76% ; All_Precision=89.06%
        3.前端运行说明：
         （1）结构：
├── frontend/                 # 前端代码文件
│   ├── static/                 # 静态文件目录 (CSS, JS, 图片)
│   │   ├── style.css           # 前端样式文件
│   │   ├── script.js           # 前端脚本文件
│   │   ├── background.jpg      # 背景图片文件
│   │   ├── cursor.png          # 自定义鼠标光标图片
│   │
│   ├── templates/              # 模板文件目录 (HTML)
│      ├── index.html          # 前端页面入口
│
├── app.py                  # Flask应用主文件
         （2）文件说明：
templates/index.html
页面中有两个主要部分：上传图片的部分和显示图片的部分；
使用函数uploadImage来处理图片上传逻辑。
static/style.css
定义界面的样式，包括背景、标题、上传部分、图片；
通过自定义的.mouse类来显示自定义鼠标光标。
static/script.js
使用document.addEventListener来监听DOM内容加载完成；
动态设置背景图片；
uploadImage函数处理文件上传，创建FormData对象，并通过fetch API发送POST请求到后端；
自定义鼠标光标，使用mousemove事件来更新鼠标位置。
app.py
Flask应用的入口文件。
使用render_template来渲染HTML模板。
upload_file视图函数处理文件上传，保存文件，并调用detection.py进行水果识别。
get_uploaded_image和get_output_image函数用于从img和output文件夹中发送图片。
         （3）界面介绍：
网页拥有静态背景图片，主体部分采用白色透明的背景板，标题为橙色的“Fruit Detection”；
Uploaded Image和Detected Image下面各有一个固定大小的图片框，
可以加载由用户上传的任意大小的图片进行加载和识别，识别前后的图片可以进行对比；
还实现了一个Q版流萤的鼠标光标
         （4） 后端：在项目根目录中运行 `python app.py` 来启动Flask服务器；
在浏览器中打开 `http://127.0.0.1:5000`，可以看到一个美观的前端界面，可以上传图片并显示结果。
由用户上传的图片会保存到img文件夹中并进行重命名（test_#.jpg),
识别后的图片同时会保存在output文件夹中，名字相同。

运行说明    
整个项目的文件放在了阿里云盘https://www.alipan.com/s/rfevUyJ4fDQ （可以不限速下载）
同时项目在组员元宇涵的github中的链接为：https://github.com/Meta217/yolov7-fruit-detection
运行时请把我们训练好的权重文件best_epoch_weights.pth放在logs文件夹中
更详细的运行说明和可以直接运行的项目文件请在项目的github链接上查看   
                              
环境说明：
        1.支持python > 3.7的环境 pytorch >1.7.0，cuda>=11.0，cudnn 8.0.5 特别说明：小组训练及测试在python 3.11环境下进行

由于模型体积过大，可能无法上传至对分易，模型所在的网盘链接为：
”
人工智能原理大作业
https://www.alipan.com/s/rfevUyJ4fDQ
点击链接保存，或者复制本段内容，打开「阿里云盘」APP ，无需下载极速在线查看，视频原画倍速播放。
“
特此对我们带来的不便表示歉意
由于初次参与大作业，可能有些地方考虑不周，如果发现模型无法运行或是其他问题，请及时与我们联系！
# yolov7-fruit-detection


<!-- PROJECT SHIELDS -->

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]

<!-- PROJECT LOGO -->
<br />

<p align="center">
  <a href="https://github.com/Meta217/yolov7-fruit-detection/">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">yolov7-fruit-detection</h3>
  <p align="center">
    使用yolov7来进行水果识别！
    <br />
    <a href="https://github.com/Meta217/yolov7-fruit-detection"><strong>探索本项目的文档 »</strong></a>
    <br />
    <br />
    <a href="https://github.com/Meta217/yolov7-fruit-detection">查看Demo</a>
    ·
    <a href="https://github.com/Meta217/yolov7-fruit-detection/issues">报告Bug</a>
    ·
    <a href="https://github.com/Meta217/yolov7-fruit-detection/issues">提出新特性</a>
  </p>

</p>

本篇README.md面向开发者

## 目录

- [yolov7-fruit-detection](#yolov7-fruit-detection)
  - [目录](#目录)
    - [文件目录说明](#文件目录说明)
    - [环境说明](#环境说明)
    - [部署](#部署)
    - [运行说明](#运行说明)
    - [前端运行说明](#前端运行说明)
      - [结构](#结构)
      - [文件说明](#文件说明)
      - [界面介绍](#界面介绍)
      - [后端运行](#后端运行)

### 文件目录说明

```
yolov7-fruit-detection/
│
├── label_data/                 # 用于存放自己标注的数据
│
│
├── logs/                 # 存放由我们小组训练好的权重文件（270mb左右）
│
│
├── utils/                # 存放模型加载、绘图以及测试数据的相关代码
│
├── test/                  # 用于存放用来测试的数据
│
├── img/                 # 可以存放供前端测试的任意图片
│
├── output/                 # 存放在前端识别后的图片
│
├── frontend/                 # 前端代码文件
│   ├── static/                 # 静态文件目录 (CSS, JS, 图片)
│   │   ├── style.css           # 前端样式文件
│   │   ├── script.js           # 前端脚本文件
│   │   ├── background.jpg      # 背景图片文件
│   │   ├── cursor.png          # 自定义鼠标光标图片
│   │
│   ├── templates/              # 模板文件目录 (HTML)
│       ├── index.html          # 前端页面入口
│
├── detection.py                # 图像识别脚本
│
├── app.py                  # Flask应用主文件
│
├── predict.py             # 用于测试数据     
│
├── train.py               # 用于训练模型    
│
├── yolo.py                # 涉及目标检测、数据测试的内容                 
│
└── ...                     # 其他项目相关文件
```

### 环境说明

1. 支持 python > 3.7 的环境，pytorch >1.7.0，cuda>=11.0，cudnn 8.0.5。
2. 特别说明：小组训练及测试在 python 3.11 环境下进行。

### 部署

```sh
git clone https://github.com/Meta217/yolov7-fruit-detection.git
```

### 运行说明
1. 在yolo.py设置model_path(logs目录训练好的权重文件)和phi(yolov7的版本)
2. 运行 `python predict.py`，终端窗口会输出 metric 的结果
3. 运行 `python app.py`, 进行前端交互
4. 终端的输出格式为：

```
"Map = class AP || score_threhold= x : F1= x ; Recall= x ; Precision= x"
```

其中，score_threhold 代表IoU，mean average precision在最左侧，例如：

```
90.52% = apple AP       ||      score_threhold=0.5 : F1=0.86 ; Recall=91.43% ; Precision=82.05%
94.80% = banana AP      ||      score_threhold=0.5 : F1=0.89 ; Recall=85.00% ; Precision=94.44%
94.53% = orange AP      ||      score_threhold=0.5 : F1=0.92 ; Recall=92.86% ; Precision=90.70%
mAP = 93.29%      ||    All_score_threhold=0.5 : F1=0.89 ; All_Recall=89.76% ; All_Precision=89.06%
```

### 前端运行说明

#### 结构

```
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
```

#### 文件说明

- `templates/index.html`
  - 页面中有两个主要部分：上传图片的部分和显示图片的部分；
  - 使用函数 `uploadImage` 来处理图片上传逻辑。

- `static/style.css`
  - 定义界面的样式，包括背景、标题、上传部分、图片；
  - 通过自定义的 `.mouse` 类来显示自定义鼠标光标。

- `static/script.js`
  - 使用 `document.addEventListener` 来监听DOM内容加载完成；
  - 动态设置背景图片；
  - `uploadImage` 函数处理文件上传，创建 `FormData` 对象，并通过 `fetch API` 发送 `POST` 请求到后端；
  - 自定义鼠标光标，使用 `mousemove` 事件来更新鼠标位置。

- `app.py`
  - Flask应用的入口文件。
  - 使用 `render_template` 来渲染HTML模板。
  - `upload_file` 视图函数处理文件上传，保存文件，并调用 `detection.py` 进行水果识别。
  - `get_uploaded_image` 和 `get_output_image` 函数用于从 `img` 和 `output` 文件夹中发送图片。

#### 界面介绍

- 网页拥有静态背景图片，主体部分采用白色透明的背景板，标题为橙色的“Fruit Detection”；
- `Uploaded Image` 和 `Detected Image` 下面各有一个固定大小的图片框，可以加载由用户上传的任意大小的图片进行加载和识别，识别前后的图片可以进行对比；
- 还实现了一个Q版流萤的鼠标光标。

#### 后端运行

- 运行 `python app.py` 来启动Flask服务器；
- 在浏览器中打开 `http://127.0.0.1:5000`，可以看到一个美观的前端界面，可以上传图片并显示结果。
- 由用户上传的图片会保存到 `img` 文件夹中并进行重命名（`test_#.jpg`），识别后的图片会保存在 `output` 文件夹中，名字相同。


<!-- links -->
[your-project-path]:Meta217/yolov7-fruit-detection
[contributors-shield]: https://img.shields.io/github/contributors/Meta217/yolov7-fruit-detection.svg?style=flat-square
[contributors-url]: https://github.com/Meta217/yolov7-fruit-detection/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Meta217/yolov7-fruit-detection.svg?style=flat-square
[forks-url]: https://github.com/Meta217/yolov7-fruit-detection/network/members
[stars-shield]: https://img.shields.io/github/stars/Meta217/yolov7-fruit-detection.svg?style=flat-square
[stars-url]: https://github.com/Meta217/yolov7-fruit-detection/stargazers
[issues-shield]: https://img.shields.io/github/issues/Meta217/yolov7-fruit-detection.svg?style=flat-square
[issues-url]: https://img.shields.io/github/issues/Meta217/yolov7-fruit-detection.svg
[license-shield]: https://img.shields.io/github/license/Meta217/yolov7-fruit-detection.svg?style=flat-square
[license-url]: https://github.com/Meta217/yolov7-fruit-detection/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/shaojintian
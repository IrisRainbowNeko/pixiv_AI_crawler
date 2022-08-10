# 人工智能pixiv高质量涩图爬虫
# 能学会你xp的AI涩图爬虫

爬虫部分基于 [PixivCrawler](https://github.com/CWHer/PixivCrawler.git) 修改实现，
涩图识别分类部分使用 [ConvNeXt](https://github.com/facebookresearch/ConvNeXt.git) 作为backbone的分类模型实现，
性能优于Trasnformer类模型。

## 自动筛选效果

<img src="imgs/c1.jpg" >

## 环境配置
环境配置参考 [ConvNeXt](https://github.com/facebookresearch/ConvNeXt.git)

需要 **pytorch==1.8 timm==0.3.2**

下载miniconda，创建新python环境并激活
```bash
conda create -n pixivai python=3.9
conda activate pixivai
```

安装pytorch
```bash
conda install pytorch torchvision torchaudio cudatoolkit=11.1 -c pytorch-lts -c conda-forge
# 没有N卡的用这个
conda install pytorch torchvision torchaudio cpuonly -c pytorch-lts
```

安装其他依赖
```bash
pip install -r requirements.txt
```

## 使用方法
下载预训练权重放在```ckpt/```文件夹内:

[下载权重-百度网盘](https://pan.baidu.com/s/1iuZktVIPGF0DONdQeGfjSw) 提取码：mmwi 或 [下载权重](https://github.com/7eu7d7/pixiv_AI_crawler/releases/download/v2/checkpoint-best_t5.pth)

根据 [PixivCrawler](https://github.com/CWHer/PixivCrawler.git) 的说明配置爬虫，设置账号和cookie，设置要爬的内容。

```pixiv_crawler/config.py```中配置爬虫基本参数。

运行命令启动AI爬虫:
```bash
# 不加关键字默认爬日榜
python AIcrawler.py --ckpt 模型权重 --n_images 总图像个数 [--keyword 关键字] 
```

## 按自己的xp训练模型

### 数据处理
准备至少5000张图。
用```labeler.py```打标签，数据集标签会储存为json格式。

**或**

把不同类别放入不同文件夹，用```labeler_folder.py```一键打标签。

```
images
|--0
|  |--1.png
|  |--2.png
|
|--1
```

用```data_proc.py```划分训练集和测试集，并对图像进行预处理。

修改参数，运行脚本训练:
```bash
python train.sh
```

训练参数设置参考 [ConvNeXt](https://github.com/facebookresearch/ConvNeXt.git)
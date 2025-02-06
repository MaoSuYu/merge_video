# 视频合并工具

一个用于合并多个MP4视频文件的Python工具。

## 目录结构

```
merge_video/
├── main.py              # 主程序入口
├── utils/              # 工具模块目录
│   ├── __init__.py     # 模块初始化文件
│   ├── logger.py       # 日志配置模块
│   ├── file_handler.py # 文件处理模块
│   ├── ffmpeg_handler.py # FFmpeg操作模块
│   └── progress.py     # 进度条模块
```

## 环境配置

```bash
# 创建conda环境
conda create -n video_merge python=3.10

# 激活环境
conda activate video_merge

# 安装依赖
conda install -c conda-forge ffmpeg
conda install tqdm

# 如果使用pip安装
pip install tqdm
```

## 使用说明

1. 将需要合并的MP4视频文件放入video目录
2. 视频文件支持两种命名方式:
   - 纯数字命名(如: 1.mp4, 2.mp4) - 将按数字顺序合并
   - 其他命名 - 将按文件名字母顺序合并
3. 运行程序:
```bash
python main.py
```
4. 根据提示输入合并后的视频文件名(直接回车将使用时间戳命名)
5. 合并后的视频将保存在output目录下
6. 详细的操作日志将保存在video_merge.log文件中,包含:
   - 视频排序信息
   - 每个视频的时长
   - 每个视频的编码信息(编码格式、分辨率、码率、帧率)
   - 合并进度和结果

## 功能特点

- 自动检测ffmpeg是否安装
- 支持大小写不敏感的mp4文件扩展名
- 实时显示合并进度条
- 自动验证输出文件完整性
- 详细的日志记录
- 自动创建所需目录结构
- 支持自定义输出文件名
- 显示每个视频的详细时长信息
- 显示每个视频的编码信息(编码、分辨率、码率、帧率)
- 默认使用时间戳命名(格式: YYYYMMDD_HHMMSS)

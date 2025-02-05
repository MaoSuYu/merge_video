import os
from .logger import logger

def create_video_dir():
    """创建video目录"""
    if not os.path.exists('video'):
        os.makedirs('video')
        logger.info("创建video目录")
    else:
        logger.info("video目录已存在")

def create_output_dir():
    """创建output目录"""
    if not os.path.exists('output'):
        os.makedirs('output')
        logger.info("创建output目录")
    else:
        logger.info("output目录已存在")

def get_video_files():
    """获取并排序video目录下的mp4文件"""
    if not os.path.exists('video'):
        logger.error("video目录不存在")
        return []
    
    # 获取所有mp4文件
    video_files = [f for f in os.listdir('video') if f.lower().endswith('.mp4')]
    if not video_files:
        logger.error("未找到mp4文件")
        return []
    
    # 检查是否所有文件都是数字命名
    all_numeric = all(f.split('.')[0].isdigit() for f in video_files)
    
    if all_numeric:
        # 如果全是数字命名,按数字大小排序
        video_files.sort(key=lambda x: int(x.split('.')[0]))
        logger.info("检测到纯数字命名,按序号排序")
    else:
        # 如果不是纯数字命名,按原始文件名排序
        video_files.sort()
        logger.info("检测到非数字命名,按文件名排序")
    
    logger.info(f"找到{len(video_files)}个视频文件: {video_files}")
    return video_files

def create_concat_file(video_files):
    """创建ffmpeg concat所需的文件列表"""
    with open('concat.txt', 'w', encoding='utf-8') as f:
        for video in video_files:
            f.write(f"file 'video/{video}'\n")
    logger.info("创建concat.txt文件")

def cleanup_concat_file():
    """清理临时文件"""
    if os.path.exists('concat.txt'):
        os.remove('concat.txt')

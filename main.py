import os
from utils.logger import logger
from utils.video_processor import get_sorted_videos
from utils.merger import merge_video_files

def main():
    """主函数"""
    logger.info("视频合并工具")
    
    # 确保目录存在
    os.makedirs('video', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    # 获取排序后的视频列表
    videos = get_sorted_videos('video')
    if not videos:
        return
    
    # 获取输出文件名
    output_name = input("\n请输入合并后的文件名(直接回车使用时间戳): ").strip()
    
    # 合并视频
    merge_video_files(videos, output_name)

if __name__ == "__main__":
    main()

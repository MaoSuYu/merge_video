from utils import (
    logger,
    check_ffmpeg,
    create_video_dir,
    create_output_dir,
    get_video_files,
    create_concat_file,
    cleanup_concat_file,
    merge_videos,
    verify_output
)
import os
from datetime import datetime

def get_output_filename():
    """获取输出文件名"""
    filename = input("请输入合并后的视频文件名(直接回车将使用时间戳): ").strip()
    
    if not filename:
        # 使用时间戳作为默认文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'merged_{timestamp}.mp4'
    elif not filename.endswith('.mp4'):
        # 确保文件名以.mp4结尾
        filename = f'{filename}.mp4'
    
    return os.path.join('output', filename)

def main():
    """主函数"""
    logger.info("开始视频合并任务")
    
    # 检查ffmpeg
    if not check_ffmpeg():
        return
    
    # 创建必要的目录
    create_video_dir()
    create_output_dir()
    
    # 获取视频文件
    video_files = get_video_files()
    if not video_files:
        return
    
    # 获取输出文件名
    output_file = get_output_filename()
    
    # 创建concat文件
    create_concat_file(video_files)
    
    try:
        # 合并视频
        if merge_videos(video_files, output_file=output_file):
            # 验证输出
            verify_output(output_file)
    finally:
        # 清理临时文件
        cleanup_concat_file()
    
    logger.info("任务结束")

if __name__ == "__main__":
    main()

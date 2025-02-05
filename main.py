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
    
    # 创建concat文件
    create_concat_file(video_files)
    
    try:
        # 合并视频
        output_file = 'output/merged_output.mp4'
        if merge_videos(video_files, output_file=output_file):
            # 验证输出
            verify_output(output_file)
    finally:
        # 清理临时文件
        cleanup_concat_file()
    
    logger.info("任务结束")

if __name__ == "__main__":
    main()

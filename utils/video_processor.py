import os
from typing import List, Optional
from .logger import logger
from .video_info import VideoInfo
from .ffmpeg_handler import get_video_duration, get_video_codec_info

def get_video_info(file_path: str, filename: str) -> Optional[VideoInfo]:
    """获取视频信息"""
    try:
        # 获取视频信息
        duration = get_video_duration(file_path)
        codec_info = get_video_codec_info(file_path)
        
        if not codec_info:
            logger.error(f"无法获取视频信息: {filename}")
            return None
        
        # 创建VideoInfo对象
        video_info = VideoInfo(
            filename=filename,
            duration=duration,
            codec=codec_info['codec'],
            width=codec_info['width'],
            height=codec_info['height'],
            bitrate=codec_info['bitrate'],
            fps=codec_info['fps'],
            path=file_path
        )
        
        # 记录视频信息
        logger.info(f"[{filename}]")
        logger.info(f"  时长: {video_info.duration_str}")
        logger.info(f"  编码: {video_info.codec}")
        logger.info(f"  分辨率: {video_info.resolution}")
        logger.info(f"  码率: {video_info.bitrate}kbps")
        logger.info(f"  帧率: {video_info.fps}fps")
        
        return video_info
            
    except Exception as e:
        logger.error(f"获取视频信息失败: {str(e)}")
        return None

def get_sorted_videos(directory: str) -> List[VideoInfo]:
    """获取排序后的视频列表"""
    # 获取视频文件列表
    video_files = [f for f in os.listdir(directory) if f.lower().endswith('.mp4')]
    if not video_files:
        logger.error("未找到MP4文件")
        return []
    
    # 检查是否所有文件都是数字命名
    all_numeric = all(f.split('.')[0].isdigit() for f in video_files)
    
    # 排序文件
    if all_numeric:
        video_files.sort(key=lambda x: int(x.split('.')[0]))
        logger.info("按数字序号排序")
    else:
        video_files.sort()
        logger.info("按文件名排序")
    
    # 获取视频信息
    videos: List[VideoInfo] = []
    logger.info("\n视频文件列表:")
    for video in video_files:
        video_path = os.path.join(directory, video)
        video_info = get_video_info(video_path, video)
        if video_info:
            videos.append(video_info)
    
    if videos:
        total_duration = sum(v.duration for v in videos)
        hours = int(total_duration // 3600)
        minutes = int((total_duration % 3600) // 60)
        seconds = int(total_duration % 60)
        logger.info(f"\n总时长: {hours:02d}:{minutes:02d}:{seconds:02d}")
    
    return videos

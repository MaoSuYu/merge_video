import os
import tempfile
from typing import List, Optional
from datetime import datetime
from .logger import logger
from .video_info import VideoInfo
from .ffmpeg_handler import merge_videos, verify_output

def merge_video_files(videos: List[VideoInfo], output_name: Optional[str] = None) -> Optional[str]:
    """合并视频文件"""
    if not videos:
        logger.error("没有视频文件可合并")
        return None
    
    if len(videos) == 1:
        logger.error("只有一个视频文件,不需要合并")
        return None
    
    # 设置输出文件名
    if not output_name:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_name = f'merged_{timestamp}.mp4'
    elif not output_name.endswith('.mp4'):
        output_name += '.mp4'
    
    output_path = os.path.join('output', output_name)
    logger.info(f"\n输出文件: {output_name}")
    
    # 在当前目录创建临时文件
    concat_file = 'temp_concat.txt'
    try:
        # 写入concat文件
        with open(concat_file, 'w', encoding='utf-8') as f:
            for video in videos:
                f.write(f"file '{video.path}'\n")
        
        logger.info("开始合并...")
        # 合并视频
        if merge_videos(videos, concat_file, output_path):
            # 验证输出
            if verify_output(output_path):
                file_size = os.path.getsize(output_path) / (1024 * 1024)  # 转换为MB
                logger.info(f"合并完成 ({file_size:.1f}MB)")
                return output_path
            else:
                logger.error("输出文件验证失败")
        else:
            logger.error("合并过程失败")
            
    except Exception as e:
        logger.error(f"合并失败: {str(e)}")
        
    finally:
        # 清理临时文件
        if os.path.exists(concat_file):
            os.remove(concat_file)
    
    return None

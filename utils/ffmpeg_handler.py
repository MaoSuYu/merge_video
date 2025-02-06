import os
import subprocess
import json
from typing import Dict, List, Optional
from .logger import logger
from .progress import ProgressBar
from .video_info import VideoInfo

def check_ffmpeg() -> bool:
    """检查系统是否安装了ffmpeg"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("FFmpeg检查通过")
        return True
    except FileNotFoundError:
        logger.error("未找到FFmpeg,请确保系统已安装FFmpeg")
        return False

def get_video_duration(video_path: str) -> float:
    """获取视频时长"""
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
           '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"ffprobe执行失败: {result.stderr}")
        return float(result.stdout)
    except Exception as e:
        logger.error(f"无法获取视频时长: {str(e)}")
        raise

def get_video_codec_info(video_path: str) -> Optional[Dict]:
    """获取视频编码信息"""
    cmd = [
        'ffprobe', 
        '-v', 'quiet',
        '-print_format', 'json',
        '-show_streams',
        '-select_streams', 'v:0',  # 只选择第一个视频流
        video_path
    ]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"ffprobe执行失败: {result.stderr}")
        
        data = json.loads(result.stdout)
        if 'streams' not in data or not data['streams']:
            raise Exception("未找到视频流信息")
        
        stream = data['streams'][0]
        return {
            'codec': stream.get('codec_name', 'unknown').upper(),
            'width': stream.get('width', 0),
            'height': stream.get('height', 0),
            'bitrate': int(stream.get('bit_rate', 0)) // 1000,  # 转换为kbps
            'fps': round(eval(stream.get('r_frame_rate', '0/1')), 2)  # 处理帧率格式(e.g., '30000/1001')
        }
    except Exception as e:
        logger.error(f"无法获取视频编码信息: {str(e)}")
        raise

def merge_videos(videos: List[VideoInfo], concat_file: str, output_file: str) -> bool:
    """合并视频文件"""
    if not check_ffmpeg():
        return False
    
    # 获取总时长用于进度条
    total_duration = sum(v.duration for v in videos)
    
    # 合并命令
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', concat_file, '-c', 'copy', output_file
    ]
    
    try:
        # 启动ffmpeg进程
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # 创建进度条
        progress_bar = ProgressBar(total_duration)
        
        # 实时更新进度条
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if "time=" in output:
                    time_str = output.split("time=")[1].split()[0]
                    progress_bar.update(time_str)
                elif "error" in output.lower():
                    logger.error(f"FFmpeg错误: {output.strip()}")
        
        progress_bar.close()
        process.wait()
        
        if process.returncode != 0:
            stderr = process.stderr.read()
            logger.error(f"FFmpeg执行失败: {stderr}")
            return False
            
        return True
            
    except Exception as e:
        logger.error(f"合并过程出错: {str(e)}")
        return False

def verify_output(output_file: str) -> bool:
    """验证输出文件"""
    if not os.path.exists(output_file):
        logger.error("输出文件不存在")
        return False
    
    try:
        cmd = ['ffprobe', output_file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            logger.error(f"输出文件验证失败: {result.stderr}")
            return False
        
        logger.info("输出文件验证通过")
        return True
        
    except Exception as e:
        logger.error(f"验证过程出错: {str(e)}")
        return False

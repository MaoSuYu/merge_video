import os
import subprocess
import json
from datetime import datetime
from .logger import logger
from .progress import ProgressBar

def check_ffmpeg():
    """检查系统是否安装了ffmpeg"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logger.info("FFmpeg检查通过")
        return True
    except FileNotFoundError:
        logger.error("未找到FFmpeg,请确保系统已安装FFmpeg")
        return False

def get_video_duration(video_path):
    """获取单个视频的时长"""
    cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
           '-of', 'default=noprint_wrappers=1:nokey=1', video_path]
    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        duration = float(result.stdout)
        return duration
    except:
        logger.error(f"无法获取视频 {video_path} 的时长")
        return 0

def get_video_codec_info(video_path):
    """获取视频的编码信息"""
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
        data = json.loads(result.stdout)
        if 'streams' in data and len(data['streams']) > 0:
            stream = data['streams'][0]
            return {
                'codec': stream.get('codec_name', 'unknown').upper(),
                'width': stream.get('width', 0),
                'height': stream.get('height', 0),
                'bitrate': int(stream.get('bit_rate', 0)) // 1000,  # 转换为kbps
                'fps': round(eval(stream.get('r_frame_rate', '0/1')), 2)  # 处理帧率格式(e.g., '30000/1001')
            }
    except Exception as e:
        logger.error(f"无法获取视频 {video_path} 的编码信息: {str(e)}")
    return None

def format_duration(seconds):
    """将秒数转换为时分秒格式"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def get_total_duration(video_files):
    """获取所有视频的总时长"""
    total_duration = 0
    for video in video_files:
        duration = get_video_duration(f'video/{video}')
        total_duration += duration
    return total_duration

def merge_videos(video_files, concat_file='concat.txt', output_file=None):
    """合并视频文件"""
    if not video_files:
        return False
    
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join('output', f'merged_{timestamp}.mp4')
    
    # 获取总时长用于进度条
    total_duration = get_total_duration(video_files)
    if total_duration == 0:
        return False
    
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
            if output and "time=" in output:
                time_str = output.split("time=")[1].split()[0]
                progress_bar.update(time_str)
        
        progress_bar.close()
        process.wait()
        
        if process.returncode == 0:
            logger.info(f"视频合并完成: {output_file}")
            return True
        else:
            logger.error("视频合并失败")
            return False
            
    except Exception as e:
        logger.error(f"合并过程出错: {str(e)}")
        return False

def verify_output(output_file=None):
    """验证输出文件"""
    if output_file is None:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_file = os.path.join('output', f'merged_{timestamp}.mp4')
    
    if not os.path.exists(output_file):
        logger.error("输出文件不存在")
        return False
    
    try:
        cmd = ['ffprobe', output_file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logger.info("输出文件验证通过")
            return True
        else:
            logger.error("输出文件验证失败")
            return False
    except Exception as e:
        logger.error(f"验证过程出错: {str(e)}")
        return False

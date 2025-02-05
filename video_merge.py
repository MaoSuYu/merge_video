import os
import sys
import subprocess
from tqdm import tqdm
import time
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('video_merge.log'),
        logging.StreamHandler()
    ]
)

def check_ffmpeg():
    """检查系统是否安装了ffmpeg"""
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        logging.info("FFmpeg检查通过")
        return True
    except FileNotFoundError:
        logging.error("未找到FFmpeg,请确保系统已安装FFmpeg")
        return False

def create_video_dir():
    """创建video目录"""
    if not os.path.exists('video'):
        os.makedirs('video')
        logging.info("创建video目录")
    else:
        logging.info("video目录已存在")

def get_video_files():
    """获取并排序video目录下的mp4文件"""
    if not os.path.exists('video'):
        logging.error("video目录不存在")
        return []
    
    # 获取所有mp4文件
    video_files = [f for f in os.listdir('video') if f.lower().endswith('.mp4')]
    if not video_files:
        logging.error("未找到mp4文件")
        return []
    
    # 检查是否所有文件都是数字命名
    all_numeric = all(f.split('.')[0].isdigit() for f in video_files)
    
    if all_numeric:
        # 如果全是数字命名,按数字大小排序
        video_files.sort(key=lambda x: int(x.split('.')[0]))
        logging.info("检测到纯数字命名,按序号排序")
    else:
        # 如果不是纯数字命名,按原始文件名排序
        video_files.sort()
        logging.info("检测到非数字命名,按文件名排序")
    logging.info(f"找到{len(video_files)}个视频文件: {video_files}")
    return video_files

def create_concat_file(video_files):
    """创建ffmpeg concat所需的文件列表"""
    with open('concat.txt', 'w', encoding='utf-8') as f:
        for video in video_files:
            f.write(f"file 'video/{video}'\n")
    logging.info("创建concat.txt文件")

def get_total_duration(video_files):
    """获取所有视频的总时长"""
    total_duration = 0
    for video in video_files:
        cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
               '-of', 'default=noprint_wrappers=1:nokey=1', f'video/{video}']
        try:
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            duration = float(result.stdout)
            total_duration += duration
        except:
            logging.error(f"无法获取视频 {video} 的时长")
            return 0
    return total_duration

def merge_videos(video_files):
    """合并视频文件"""
    if not video_files:
        return False
    
    # 获取总时长用于进度条
    total_duration = get_total_duration(video_files)
    if total_duration == 0:
        return False

    # 创建concat文件
    create_concat_file(video_files)
    
    # 合并命令
    output_file = 'merged_output.mp4'
    cmd = [
        'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
        '-i', 'concat.txt', '-c', 'copy', output_file
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
        pbar = tqdm(total=100, desc="合并进度")
        last_progress = 0
        
        # 实时更新进度条
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                if "time=" in output:
                    time_str = output.split("time=")[1].split()[0]
                    hours, minutes, seconds = map(float, time_str.split(':'))
                    current_duration = hours * 3600 + minutes * 60 + seconds
                    progress = min(100, int((current_duration / total_duration) * 100))
                    if progress > last_progress:
                        pbar.update(progress - last_progress)
                        last_progress = progress
        
        pbar.close()
        process.wait()
        
        if process.returncode == 0:
            logging.info("视频合并完成")
            # 清理临时文件
            os.remove('concat.txt')
            return True
        else:
            logging.error("视频合并失败")
            return False
            
    except Exception as e:
        logging.error(f"合并过程出错: {str(e)}")
        return False

def verify_output():
    """验证输出文件"""
    if not os.path.exists('merged_output.mp4'):
        logging.error("输出文件不存在")
        return False
    
    try:
        cmd = ['ffprobe', 'merged_output.mp4']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            logging.info("输出文件验证通过")
            return True
        else:
            logging.error("输出文件验证失败")
            return False
    except Exception as e:
        logging.error(f"验证过程出错: {str(e)}")
        return False

def main():
    """主函数"""
    logging.info("开始视频合并任务")
    
    # 检查ffmpeg
    if not check_ffmpeg():
        return
    
    # 创建video目录
    create_video_dir()
    
    # 获取视频文件
    video_files = get_video_files()
    if not video_files:
        return
    
    # 合并视频
    if merge_videos(video_files):
        # 验证输出
        verify_output()
    
    logging.info("任务结束")

if __name__ == "__main__":
    main()

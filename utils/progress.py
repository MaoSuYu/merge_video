from tqdm import tqdm

class ProgressBar:
    def __init__(self, total_duration):
        """初始化进度条"""
        self.pbar = tqdm(total=100, desc="合并进度")
        self.total_duration = total_duration
        self.last_progress = 0

    def update(self, time_str):
        """更新进度条"""
        try:
            hours, minutes, seconds = map(float, time_str.split(':'))
            current_duration = hours * 3600 + minutes * 60 + seconds
            progress = min(100, int((current_duration / self.total_duration) * 100))
            
            if progress > self.last_progress:
                self.pbar.update(progress - self.last_progress)
                self.last_progress = progress
        except:
            pass

    def close(self):
        """关闭进度条"""
        self.pbar.close()

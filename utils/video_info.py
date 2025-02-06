from dataclasses import dataclass

@dataclass
class VideoInfo:
    """视频信息数据类"""
    filename: str
    duration: float
    codec: str
    width: int
    height: int
    bitrate: int
    fps: float
    path: str

    @property
    def resolution(self) -> str:
        """获取分辨率字符串"""
        return f"{self.width}x{self.height}"
    
    @property
    def duration_str(self) -> str:
        """获取格式化的时长字符串"""
        hours = int(self.duration // 3600)
        minutes = int((self.duration % 3600) // 60)
        seconds = int(self.duration % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    @property
    def info_str(self) -> str:
        """获取格式化的视频信息字符串"""
        return (f"{self.codec} {self.resolution} "
                f"{self.bitrate}kbps {self.fps}fps")

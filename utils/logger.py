import logging
import sys
from datetime import datetime

# 创建日志格式化器
class CustomFormatter(logging.Formatter):
    """自定义日志格式化器"""
    
    def __init__(self):
        super().__init__()
        self.datefmt = '%Y-%m-%d %H:%M:%S'
        
        # 不同级别的日志前缀
        self.prefixes = {
            logging.DEBUG: '🔍 ',
            logging.INFO: '✓ ',
            logging.WARNING: '⚠️ ',
            logging.ERROR: '❌ ',
            logging.CRITICAL: '🔥 '
        }
    
    def format(self, record):
        # 添加前缀
        prefix = self.prefixes.get(record.levelno, '')
        
        # 格式化时间
        timestamp = datetime.fromtimestamp(record.created).strftime(self.datefmt)
        
        # 根据日志级别使用不同格式
        if record.levelno == logging.INFO:
            # INFO级别简化显示
            return f"{prefix}{record.getMessage()}"
        else:
            # 其他级别显示时间和级别
            level_name = record.levelname.capitalize()
            return f"{timestamp} [{level_name}] {prefix}{record.getMessage()}"

# 创建日志处理器
def setup_logger():
    """配置日志记录器"""
    logger = logging.getLogger('video_merge')
    logger.setLevel(logging.INFO)
    
    # 清除现有的处理器
    logger.handlers.clear()
    
    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(CustomFormatter())
    logger.addHandler(console_handler)
    
    # 文件处理器
    file_handler = logging.FileHandler('video_merge.log', encoding='utf-8')
    file_handler.setFormatter(
        logging.Formatter(
            '%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    )
    logger.addHandler(file_handler)
    
    return logger

# 创建日志记录器实例
logger = setup_logger()

from datetime import datetime
from enum import Enum
import json
import sys


class LogLevel(str, Enum):
  INFO = "INFO"
  WARNING = "WARNING"
  ERROR = "ERROR"
  DEBUG = "DEBUG"

class Logger:
  def __init__(self, level: LogLevel = LogLevel.INFO):
    self.level = level
    self.level_order = {
      LogLevel.INFO: 10,
      LogLevel.DEBUG: 20,
      LogLevel.WARNING: 30,
      LogLevel.ERROR: 40,
    }

  def log(self, level: LogLevel, message: str, **kwargs):
    if self.level_order[level] < self.level_order[self.level]:
      return
    
    log_entry = {
      "timestamp": datetime.now().isoformat(),
      "level": level,
      "message": message,
      "extra": kwargs
    }

    sys.stdout.write(json.dumps(log_entry) + "\n")

  def info(self, msg, **kwargs): self.log(LogLevel.INFO, msg, **kwargs)
  def warning(self, msg, **kwargs): self.log(LogLevel.WARNING, msg, **kwargs)
  def error(self, msg, **kwargs): self.log(LogLevel.ERROR, msg, **kwargs)
  def debug(self, msg, **kwargs): self.log(LogLevel.DEBUG, msg, **kwargs)

log = Logger(level=LogLevel.DEBUG)

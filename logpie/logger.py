from datetime import datetime, timezone
from enum import Enum
import json
import os
import sys
from logpie.context import request_id
from logpie.masking.engine import MaskingEngine

class LogLevel(str, Enum):
  INFO = "INFO"
  WARNING = "WARNING"
  ERROR = "ERROR"
  DEBUG = "DEBUG"
  CRITICAL = "CRITICAL"

class Logger:
  def __init__(self, level: LogLevel = LogLevel.INFO):
    self.level = level
    self.level_order = {
        LogLevel.DEBUG: 10,
        LogLevel.INFO: 20,
        LogLevel.WARNING: 30,
        LogLevel.ERROR: 40,
        LogLevel.CRITICAL: 50,
    }
    self.masking = MaskingEngine()

  def log(self, level: LogLevel, message: str, **kwargs):
    if self.level_order[level] < self.level_order[self.level]:
      return

    log_entry = {
      "request_id": request_id.get(None),
      "timestamp": datetime.now(timezone.utc).isoformat(),
      "level": level,
      "message": message,
      "extra": kwargs
    }
    log_entry_json = json.dumps(self.masking.mask_log_entry(log_entry), ensure_ascii=False) + "\n"

    sys.stdout.write(log_entry_json)
    self.write_file(log_entry_json)

  def info(self, msg, **kwargs): self.log(LogLevel.INFO, msg, **kwargs)
  def warning(self, msg, **kwargs): self.log(LogLevel.WARNING, msg, **kwargs)
  def error(self, msg, **kwargs): self.log(LogLevel.ERROR, msg, **kwargs)
  def debug(self, msg, **kwargs): self.log(LogLevel.DEBUG, msg, **kwargs)

  def write_file(self, log):
    try:
      os.makedirs("logs", exist_ok=True)
      today = datetime.now().strftime("%Y-%m-%d")
      path = os.path.join("logs", f"{today}.log")
      with open(path, "a") as file:
          file.write(log)
    except Exception as e:
      print(f"Failed to write file: {e}")

log = Logger(level=LogLevel.DEBUG)

import logging
import sys
from config import Config

# It's generally better to configure logging once. For this scenario, we will configure
# the specific logger to prevent duplicate handlers and propagation.

class MyLogger():
  def __init__(self,outputstream):
    # Get the logger for this specific class
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(Config.LogLevel)  # Use the log level from Config

    # Prevent messages from propagating to the root logger to avoid duplicate output
    # if the root logger also has handlers (e.g., from logging.basicConfig).
    self.logger.propagate = False

    # Add a handler only if one isn't already present for this logger
    if not self.logger.handlers:
        handler = logging.StreamHandler(outputstream)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    self.logger.info("MyLogger class initialized.")

  def info(self,message):
    self.logger.info(message)
    return

  def warning(self,message):
    self.logger.warning(message)
    return

  def error(self,message):
    self.logger.error(message)
    return
  
  def debug(self,message):
    self.logger.debug(message)
    return
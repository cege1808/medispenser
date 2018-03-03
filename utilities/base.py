import logging

loggers = {}

class Base():

  def __init__(self):
    self.logger = self.initialize_logger()

  def initialize_logger(self):
    global loggers
    class_name = self.__class__.__name__

    if loggers.get(class_name):
      return loggers.get(class_name)
    else:
      logger = logging.getLogger(self.__class__.__name__)
      logger.setLevel(logging.INFO)
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
      ch.setFormatter(formatter)
      logger.addHandler(ch)
      loggers.update({class_name: logger})
      return logger


  def logger(self):
    return self.logger

  def info(self, message):
    self.logger.info(message)

  def debug(self, message):
    self.logger.debug(message)

  def warn(self, message):
    self.logger.warn(message)

  def error(self, message):
    self.logger.error(message)

  def critical(self, message):
    self.logger.critical(message)

  def setLogLevel(self, level):
    if level == 'info':
      self.logger.setLevel(logging.INFO)
    elif level == 'debug':
      self.logger.setLevel(logging.DEBUG)
    elif level == 'warn':
      self.logger.setLevel(logging.WARN)
    elif level == 'error':
      self.logger.setLevel(logging.ERROR)
    elif level == 'critical':
      self.logger.setLevel(logging.CRITICAL)

if __name__ == '__main__':
  Base()

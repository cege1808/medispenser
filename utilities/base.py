import logging


class Base():

  def __init__(self):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    ch.setFormatter(formatter)
    self.logger.addHandler(ch)

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

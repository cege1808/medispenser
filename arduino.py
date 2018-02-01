import time
import serial
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

class Arduino(Base):

  def __init__(self, user_id):
    Base.__init__(self)
    self.setLogLevel('debug')
    self.user_id = user_id
    self.pill_queue = []

  def initialize_serial(self):
    addresses = ['tty.usbmodem1411', 'tty.usbmodem1421']
    for address in addresses:
      try:
        self.serial = serial.Serial("/dev/{}".format(address), 9600)
        self.debug("successfully open port at /dev/{}".format(address))
        time.sleep(2)
        return
      except:
        self.debug("failed to open port at /dev/{}".format(address))

  def write_serial(self, char):
    self.serial.write(char.encode())

  def write_line(self, message):
    for char in message:
      self.write_serial(char)

  def read_serial(self, *num):
    if num:
      line = self.serial.read(num)
    else:
      line = self.serial.readline()
    self.debug(line.strip())
    return line

  def turn_on_led(self):
    self.write_line('<LH>')
    self.read_serial()

  def turn_off_led(self):
    self.write_line('<LL>')
    self.read_serial()

  def blink_led(self):
    self.debug("blink")
    self.turn_off_led()
    self.turn_on_led()
    time.sleep(1)
    self.turn_off_led()

  def drop_pill(self):
    self.debug("rotate once from container")
    self.debug("check if pill has dropped")

  def close_serial(self):
    self.serial.close()

  def flush(self):
    self.serial.reset_input_buffer()
    self.serial.reset_output_buffer()

arduino = Arduino('1234')
arduino.initialize_serial()
arduino.blink_led()
arduino.close_serial()


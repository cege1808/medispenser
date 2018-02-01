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

class Serial(Base):

  def __init__(self, *address):
    Base.__init__(self)
    self.set_addresses(address or None)
    self.initialize_serial()

  def set_addresses(self, *address):
    common_addresses = ['tty.usbmodem1411', 'tty.usbmodem1421']
    if address is not None:
      self.addresses = common_addresses + [address]
    else:
      self.addresses = common_addresses

  def initialize_serial(self):
    for address in self.addresses:
      try:
        self.serial = serial.Serial("/dev/{}".format(address), 9600)
        self.info("Successfully open port at /dev/{}".format(address))
        time.sleep(2)
        return
      except:
        self.debug("Failed to open port at /dev/{}".format(address))
    self.info("Failed to any open port")

  def write(self, char):
    self.serial.write(char.encode())

  def write_char(self, char):
    self.write(char)

  def write_line(self, message):
    for char in message:
      self.write_char(char)

  def read(self, *num):
    if num:
      line = self.serial.read(num)
    else:
      line = self.serial.readline()
    self.debug(line.strip())
    return line.strip()

  def flush(self):
    self.serial.reset_input_buffer()
    self.serial.reset_output_buffer()

  def close(self):
    self.serial.close()

class Arduino(Base):

  def __init__(self, user_id):
    Base.__init__(self)
    self.setLogLevel('debug')
    self.user_id = user_id
    self.instruction_queue = []
    self.serial = Serial()

  def reset_instruction_queue(self):
    self.instruction_queue = []

  def turn_on_led(self):
    self.serial.write_line('<LH>')
    self.serial.read()

  def turn_off_led(self):
    self.serial.write_line('<LL>')
    self.serial.read()

  def blink_led(self):
    self.debug("blink")
    self.turn_off_led()
    self.turn_on_led()
    time.sleep(1)
    self.turn_off_led()

  def drop_pill(self):
    self.debug("rotate once from container")

  def verify_pill(self):
    self.debug("check if pill has dropped")

  def pill_cycle(self):
    self.drop_pill()
    self.verify_pill()

  def close(self):
    self.serial.close()


arduino = Arduino('1234')
arduino.blink_led()
arduino.close()


import time
import serial
from base import Base

class Serial(Base):

  def __init__(self, *address):
    super().__init__()
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
        self.serial = serial.Serial("/dev/{}".format(address), 9600, timeout=0)
        self.info("Successfully open port at /dev/{}".format(address))
        time.sleep(2)
        return
      except serial.SerialException:
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

  def is_open(self):
    return self.serial.is_open

  def close(self):
    self.serial.close()

class Arduino(Base):

  def __init__(self):
    super().__init__()
    self.setLogLevel('debug')
    self.serial = Serial()

  def turn_on_led(self):
    self.serial.write_line('<LH>')
    expected_reply = '[LH]'
    self.confirm_response(expected_reply)

  def turn_off_led(self):
    self.serial.write_line('<LL>')
    expected_reply = '[LL]'
    self.confirm_response(expected_reply)

  def blink_led(self):
    self.debug("blink")
    self.turn_off_led()
    self.turn_on_led()
    time.sleep(1)
    self.turn_off_led()

  def drop_pill(self, module_num):
    instruction = '<D{}>'.format(module_num)
    self.serial.write_line(instruction)
    expected_reply = '[D{}]'.format(module_num)
    self.confirm_response(expected_reply)
    self.debug("rotate once from container")

  def verify_pill(self, module_num):
    instruction = '<V{}>'.format(module_num)
    self.serial.write_line(instruction)
    expected_reply = '[V{}]'.format(module_num)
    self.confirm_response(expected_reply)
    self.debug("check if pill has dropped")

  def pill_cycle(self, module_num):
    self.drop_pill(module_num)
    self.verify_pill(module_num)

  def is_open(self):
    return self.serial.is_open()

  def close(self):
    self.serial.close()

  def confirm_response(self, expected_reply):
    # assume that response is always true
    # TODO edge cases when response is an int or false etc
    wait = True
    while wait:
      read_line = self.serial.read().decode("utf-8")
      self.debug('response: {}, expectation: {}'.format(read_line, expected_reply))
      if read_line == expected_reply:
        wait = False
      time.sleep(1)

if __name__ == '__main__':
  Arduino()




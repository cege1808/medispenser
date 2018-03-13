import time
import serial
from utilities.base import Base

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
    try:
      self.serial.close()
    except Exception:
      self.debug("No serial to close")

class Arduino(Base):

  def __init__(self):
    super().__init__()
    self.setLogLevel('debug')
    self.serial = Serial()

  def is_open(self):
    return self.serial.is_open()

  def close(self):
    self.serial.close()

  def turn_on_led(self):
    instruction = '<LH>'
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def turn_off_led(self):
    instruction = '<LL>'
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def blink_led(self):
    instruction = '<LB>'
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def wait_button_pressed(self):
    instruction = '<B>'
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def alert_and_wait_button_pressed(self):
    instruction = '<A>'
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def calibrate_motor_pos(self, module_num, current_pos):
    # current_position is num of degrees to the clockwise direction
    instruction = '<C{}{}>'.format(module_num, current_pos)
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def prepare_drop_pill(self, module_num):
    instruction = '<P{}>'.format(module_num)
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def repeat_prepare_drop_pill(self, module_num):
    instruction = '<R{}>'.format(module_num)
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def drop_pill(self, module_num):
    instruction = '<D{}>'.format(module_num)
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def verify_pill(self, module_num):
    instruction = '<V{}>'.format(module_num)
    self.serial.write_line(instruction)
    return self.get_response(instruction)

  def prepare_and_verify(self, module_num):
    self.prepare_drop_pill(module_num)
    self.debug('Pill is prepared')

    for i in range(5):
      pill_status = self.verify_pill(module_num)
      self.debug('Pill status: {}'.format(pill_status))

      if pill_status:
        self.debug('Pill successfully prepeared')
        return
      else:
        self.info('Arduino did not verify pill, try again')
        self.repeat_prepare_drop_pill(module_num)
        self.debug('Pill is prepared (repeated)')

    self.info('Please refill module {}'.format(module_num))


  def pill_cycle(self, module_num):
    if self.prepare_drop_pill(module_num):
      self.debug('Pill is prepared')

      for i in range(5):
        pill_status = self.verify_pill(module_num)
        self.debug('Pill status: {}'.format(pill_status))

        if pill_status:
          self.drop_pill(module_num)
          self.debug('Pill successfully dropped')
          return
        else:
          self.info('Arduino did not verify pill, try again')
          self.repeat_prepare_drop_pill(module_num)
          self.debug('Pill is prepared (repeated)')

      self.info('Please refill module {}'.format(module_num))
      return

    else:
      self.info('Arduino did not run instruction to prepare pill drop')

  def get_response(self, req):
    wait = True
    while wait:
      res = self.serial.read().decode("utf-8")
      self.debug('req: {}, res: {}'.format(req, res))
      if self.verify_valid_response(req, res):
        wait = False
      time.sleep(1)
    return (res[3] == 'Y')

  def verify_valid_response(self, req, res):
    if (len(res) > 0):
      if (res[0] == '[') and (res[-1] == ']'):
        if (res[1] == req[1]) and (res[2] == req[2]):
          return True
    return False


if __name__ == '__main__':
  Arduino()




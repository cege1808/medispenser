from utilities.base import Base
from utilities.arduino import Arduino
from utilities.scheduler import Scheduler

class TaskManager(Base):

  """
  issue job: self.instruction_append(job)
  completed job: self.instruction_queue.pop(0)
  example db_dict:
  # self.db_dict = [{'category': 'second', 'day': None, 'time': None, 'counter': 10, 'module_nums': [0]}]
  # self.db_dict = [{'category': 'once', 'day': None, 'time': '22:57', 'counter': None, 'module_nums': [0,1]}]
  # self.db_dict = [{'category': 'second', 'day': None, 'time': None, 'counter': 10, 'module_nums': [0,1]},
  #                 {'category': 'once', 'day': None, 'time': '23:02', 'counter': None, 'module_nums': [2]}]

  """

  def __init__(self):
    super().__init__()
    self.instruction_queue = []
    self.arduino = Arduino()
    self.scheduler = Scheduler(self.create_instruction)

  def setup_scheduler(self, db_dict):
    self.scheduler.setup(db_dict)

  def create_instruction(self, array_modules):
    self.debug("append array modules: {}".format(array_modules))
    self.instruction_queue.append(array_modules)

  def remove_nth_instruction(self, n):
    self.instruction_queue.pop(n)

  def instruction_available(self):
    return len(self.instruction_queue) > 0

  def serial_is_open(self):
    return self.arduino.is_open()

  def instruction_interrupt(self, array_modules):
     self.create_instruction(array_modules)

  def run_instruction(self, array_modules):
    self.create_instruction(array_modules)
    for module_num in self.instruction_queue[0]:
        self.arduino.pill_cycle(module_num)
        self.remove_nth_instruction(0)
        self.arduino.blink_led()
    self.arduino.close()


class ContinuousTaskManager(TaskManager):

  def __init__(self):
    super().__init__()
    # TODO self.db_dict = self.scheduler.query_db()
    db_dict = [{'category': 'second', 'day': None, 'time': None, 'counter': 10, 'module_nums': [0]}]
    self.setup_scheduler(db_dict)
    self.main_loop()

  def main_loop(self):
    while True:
      self.scheduler.run_pending()
      if self.instruction_available() and self.serial_is_open():
        for module_num in self.instruction_queue[0]:
          self.arduino.pill_cycle(module_num)
        self.remove_nth_instruction(0)
        self.arduino.blink_led()

      elif self.instruction_available():
        # TODO restart serial if not available
        pass

class LoggingDemo(TaskManager):

  def __init__(self):
    super().__init__()
    db_dict = [{'category': 'minute', 'day': None, 'time': None, 'counter': 2, 'module_nums': [0]}]
    self.setup_scheduler(db_dict)
    self.initialize_pill()
    self.main_loop()

  def initialize_pill():
    self.arduino.prepare_and_verify(self.module_num)

  def main_loop(self):
    while True:
      self.scheduler.run_pending()
      if self.instruction_available() and self.serial_is_open():
        self.arduino.wait_button_pressed()
        self.arduino.turn_on_led()
        for module_num in self.instruction_queue[0]:
          self.arduino.drop_pill(module_num)
          self.debug('Pill successfully dropped')
          self.arduino.prepare_and_verify(self.module_num)

        self.arduino.turn_off_led()
        self.remove_nth_instruction(0)
        # TODO log info to database

      elif self.instruction_available():
        # TODO restart serial if not available
        pass

class ButtonTriggerDemo(TaskManager):

  def __init__(self, module_num=0):
    super().__init__()
    self.module_num = module_num
    self.info("module number {}".format(self.module_num))
    self.initialize_pill()
    self.main_loop()

  def initialize_pill(self):
    self.arduino.prepare_and_verify(self.module_num)

  def main_loop(self):
    button_pressed = False
    while True:
      if(not button_pressed):
        self.arduino.turn_on_led()
        if (self.arduino.wait_button_pressed()):
          button_pressed = True
      else:
        self.arduino.drop_pill(self.module_num)
        self.debug('Pill successfully dropped')
        self.arduino.turn_off_led()
        self.arduino.prepare_and_verify(self.module_num)
        button_pressed = False



if __name__ == '__main__':
  ContinuousTaskManager()


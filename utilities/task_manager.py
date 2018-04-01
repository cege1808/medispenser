from utilities.base import Base
from utilities.arduino import Arduino
from utilities.scheduler import Scheduler
import sqlite3
import simpleaudio as sa


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
    self.username = "logging_demo"
    self.wave_obj = sa.WaveObject.from_wave_file('static/sound/nice_text_reminder.wav')
    # db_dict = self.get_schedule(self.username)

    db_dict = [
          {'category': 'second', 'day': None, 'time': None, 'counter': 15, 'module_nums': [0]},
          {'category': 'second', 'day': None, 'time': None, 'counter': 45, 'module_nums': [1]},
        ]
    self.setup_scheduler(db_dict)
    self.info(db_dict)
    self.initialize_pill()
    self.main_loop()

  def save_log(self, username, module_num):
    sqlite_file = '../medispenser/db.sqlite3'
    user_table = 'auth_user'
    medication_table = 'core_medication'
    log_table = 'core_log'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute(self.sql_select_statement("id", user_table, cn="username", query=username))
    user_id = c.fetchall()[0][0]
    c.execute(self.sql_select_statement("id", medication_table, cn1="user_id", query1=user_id, cn2="module_num", query2=module_num))
    medication_id = c.fetchall()[0][0]
    c.execute('INSERT OR IGNORE INTO {tn} ({cn1}, {cn2}, "created_at") VALUES ({v1}, {v2}, DATETIME("NOW"))'\
      .format(tn=log_table, cn1="medication_id", v1=medication_id, cn2="user_id", v2=user_id))
    conn.commit()
    conn.close()

  def get_schedule(self, username):
    sqlite_file = '../medispenser/db.sqlite3'
    user_table = 'auth_user'
    schedule_table = 'core_schedule'
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()
    c.execute(self.sql_select_statement("id", user_table, cn="username", query=username))
    user_id = c.fetchall()[0][0]
    c.execute(self.sql_select_statement("*", schedule_table, cn="user_id", query=user_id))
    schedules = c.fetchall()
    db_dict = []
    for schedule in schedules:
      db_dict.append({
        'category': schedule[1],
        'day': self.abbrv_to_full_day(schedule[2]),
        'time': schedule[6],
        'counter': schedule[3],
        'module_nums': schedule[4].split(',')
        })
    conn.close()
    return db_dict

  def sql_select_statement(self, col, tn, **params):
    if 'cn' in params:
      cn = params['cn']
      query = self.prepare_query(params['query'])
      return 'SELECT {col} FROM {tn} WHERE {cn}={query}'.format(col=col, tn=tn, cn=cn, query=query)
    elif 'cn1' in params:
      cn1 = params['cn1']
      query1 = self.prepare_query(params['query1'])
      cn2 = params['cn2']
      query2 = self.prepare_query(params['query2'])
      return 'SELECT {col} FROM {tn} WHERE {cn1}={query1} AND {cn2}={query2}'.format(col=col, tn=tn, cn1=cn1, query1=query1, cn2=cn2, query2=query2)
    else:
      return 'SELECT {col} FROM {tn}'.format(col=col, tn=tn)

  def prepare_query(self, query):
    if isinstance(query, str):
      query_string = "'" + query + "'"
    else:
      query_string = query
    return query_string

  def abbrv_to_full_day(self, abbrv):
    if abbrv == 'mon':
      return 'monday'
    elif abbrv == 'tue':
      return 'tuesday'
    elif abbrv == 'wed':
      return 'wednesday'
    elif  abbrv == 'thu':
      return 'thursday'
    elif  abbrv == 'fri':
      return 'friday'
    elif abbrv == 'sat':
      return 'saturday'
    elif abbrv == 'sun':
      return 'sunday'
    else:
      return abbrv

  def initialize_pill(self):
    self.arduino.prepare_and_verify(0)
    self.arduino.prepare_and_verify(1)

  def main_loop(self):
    try:
      button_pressed = False
      while True:
        self.scheduler.run_pending()
        if self.instruction_available() and self.serial_is_open():

          if(not button_pressed):
            self.arduino.turn_on_led()
            self.play_obj = self.wave_obj.play()
            if (self.arduino.wait_button_pressed()):
              button_pressed = True
              if self.play_obj.is_playing():
                self.play_obj.stop()
          else:
            self.arduino.turn_off_led()

            for module_num in self.instruction_queue[0]:
              self.arduino.drop_pill(module_num)
              self.debug('Pill successfully dropped')
              self.save_log(self.username, module_num)
              self.arduino.prepare_and_verify(module_num)

            self.remove_nth_instruction(0)
            button_pressed = False

        elif self.instruction_available():
          # TODO restart serial if not available
          pass
    except Exception as err:
      self.info(err)

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


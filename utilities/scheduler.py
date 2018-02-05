import schedule
import time
from base import Base

class Scheduler(Base):

  """
  DB Query dict structure:
    {
      category: 'week' (week, day, hour, minute, second, once),
      day: 'monday' (if category is [week, once]),
      time: '23:59' (if category is [week, day, once]),
      counter: int (if category is [hour, minute, second]),
      module_nums: [0, 1] (a list of ints),
    }

  """

  def __init__(self, instruction_fcn):
    super().__init__()
    self.setLogLevel('debug')
    self.instruction_fcn = instruction_fcn
    self.schedule = schedule

  def run_pending(self):
    self.schedule.run_pending()

  def query_db(self):
    # TODO get a list [], of dictionaries {}
    pass

  def create_instruction(self, array_modules, once_bool):
    self.instruction_fcn(array_modules)
    if once_bool:
      self.schedule.clear('once')

  def setup(self, array_db_dict):
    for db_dict in array_db_dict:
      self.setup_each_dict(db_dict)

    self.debug(self.schedule.jobs)

  def setup_each_dict(self, db_dict):
    category = db_dict['category']
    day = db_dict['day'] or None
    time = db_dict['time'] or None
    counter = db_dict['counter'] or 1
    array_modules = db_dict['module_nums']
    once_bool = category == 'once'

    if category == 'week':
      if day == 'monday':
        self.schedule.every().monday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'tuesday':
        self.schedule.every().tuesday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'wednesday':
        self.schedule.every().wednesday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'thursday':
        self.schedule.every().thursday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'friday':
        self.schedule.every().friday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'saturday':
        self.schedule.every().saturday.at(time).do(self.create_instruction, array_modules, once_bool)
      elif day == 'sunday':
        self.schedule.every().sunday.at(time).do(self.create_instruction, array_modules, once_bool)
      else:
        self.schedule.every(counter).week.at(time).do(self.create_instruction, array_modules, once_bool)

    elif category == 'day':
      self.schedule.every(counter).day.at(time).do(self.create_instruction, array_modules, once_bool)

    elif category == 'hour':
      self.schedule.every(counter).hours.do(self.create_instruction, array_modules, once_bool)

    elif category == 'minute':
      self.schedule.every(counter).minutes.do(self.create_instruction, array_modules, once_bool)

    elif category == 'second':
      self.schedule.every(counter).seconds.do(self.create_instruction, array_modules, once_bool)

    elif category == 'once':
      self.schedule.every().day.at(time).do(self.create_instruction, array_modules, once_bool).tag('once')


if __name__ == '__main__':
  Scheduler()


from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from utilities.task_manager import TaskManager

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medispenser.settings')

app = Celery('medispenser')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(queue="run_motor")
def run_motor(module_nums):
  manager = TaskManager()
  manager.run_instruction(module_nums)
  print("Successfully drop pill {}".format(module_nums))
  return {"instruction": "run_motor", "success": True, "module_nums": module_nums}


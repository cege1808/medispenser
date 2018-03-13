from django.core.management.base import BaseCommand, CommandError
from utilities.task_manager import TaskManagerButtonTrigger
import argparse

class Command(BaseCommand):
    help = 'Run task manager and trigger pill drop with a button'

    def handle(self, *args, **options):
      manager = TaskManagerButtonTrigger()

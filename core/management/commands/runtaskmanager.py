from django.core.management.base import BaseCommand, CommandError
from utilities.task_manager import ContinuousTaskManager
import argparse

class Command(BaseCommand):
    help = 'Run continuous task manager for schedule and arduino'

    def handle(self, *args, **options):
      manager = ContinuousTaskManager()

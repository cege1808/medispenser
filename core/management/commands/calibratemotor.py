from django.core.management.base import BaseCommand, CommandError
from utilities.calibration import MotorCalibration
import argparse
import sys
import signal
signal.signal(signal.SIGINT, lambda x,y: sys.exit(0))

class Command(BaseCommand):
    help = 'Calibrates motor via arduino'

    def add_arguments(self, parser):
        parser.add_argument(
            '--module_num',
            dest='module_num',
            help="module number to change motor angle",
            type=int,
        )

        parser.add_argument(
            '--current_position',
            dest='current_position',
            help="current position in degrees clockwise direction",
            type=int,
        )

    def handle(self, *args, **options):
        if options['module_num'] is not None and options['current_position'] is not None:
            MotorCalibration(module_num=options['module_num'], current_position=options['current_position'])
        elif options['module_num'] is not None:
            MotorCalibration(module_num=options['module_num'])
        else:
            MotorCalibration()

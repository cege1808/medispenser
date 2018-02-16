import sys
from base import Base
from arduino import Arduino


class bash_colors:
    '''Colors class:
    reset all colors with colors.reset
    two subclasses fg for foreground and bg for background.
    use as colors.subclass.colorname.
    i.e. colors.fg.red or colors.bg.green
    also, the generic bold, disable, underline, reverse, strikethrough,
    and invisible work with the main class
    i.e. colors.bold
    '''
    reset='\033[0m'
    bold='\033[01m'
    disable='\033[02m'
    italic='\033[03m'
    underline='\033[04m'
    reverse='\033[07m'
    strikethrough='\033[09m'
    invisible='\033[08m'
    class fg:
        black='\033[30m'
        red='\033[31m'
        green='\033[32m'
        orange='\033[33m'
        blue='\033[34m'
        purple='\033[35m'
        cyan='\033[36m'
        lightgrey='\033[37m'
        darkgrey='\033[90m'
        lightred='\033[91m'
        lightgreen='\033[92m'
        yellow='\033[93m'
        lightblue='\033[94m'
        pink='\033[95m'
        lightcyan='\033[96m'
    class bg:
        black='\033[40m'
        red='\033[41m'
        green='\033[42m'
        orange='\033[43m'
        blue='\033[44m'
        purple='\033[45m'
        cyan='\033[46m'
        darkgrey='\033[100m'
        lightred='\033[101m'
        lightgreen='\033[102m'
        yellow='\033[103m'
        lightblue='\033[104m'
        pink='\033[105m'
        lightcyan='\033[106m'

class MotorCalibration(Base):

  def __init__(self):
    super().__init__()
    self.intro()
    self.arduino = Arduino()
    self.module_num_input()

  def pretty_print(self, text, color):
    print(color + text + bash_colors.reset)

  def pretty_input(self, prompt, color):
    return input(color + prompt + bash_colors.reset)

  def intro(self):
    self.pretty_print("  Welcome to Medispenser's Motor Calibration  \n", bash_colors.reverse)
    self.pretty_print("  This script calibrates the shaft to position 0", bash_colors.fg.lightgreen)
    self.pretty_print("  When the shaft is pointing to the top of the motor, it is at position 0", bash_colors.fg.lightgreen)
    self.pretty_print("  and increments the position (up to 360 degrees) in the clockwise direction." , bash_colors.fg.lightgreen)

  def module_num_input(self):
    module_num = self.pretty_input("\n  Please enter the module number wants to be calibrate: ", bash_colors.fg.orange)
    try:
      int(module_num)
      self.pretty_print("  The current module num is {} ".format(module_num), bash_colors.fg.yellow)
      self.current_module_num = module_num
    except ValueError:
      self.pretty_print("  Module num is not an integer, try again..", bash_colors.fg.orange)
      self.module_num_input()

    self.pos_input()

  def pos_input(self):
    pos = self.pretty_input("\n  Please enter the current position of the shaft: ", bash_colors.fg.lightblue)
    try:
      int(pos)
      self.pretty_print("  The current shaft position is {} ".format(pos), bash_colors.fg.lightcyan)
      self.current_pos = str(pos).zfill(3)
    except ValueError:
      self.pretty_print("  Position is not an integer, try again..", bash_colors.fg.lightblue)
      self.pos_input()

    self.move_motor()

  def move_motor(self):
    self.pretty_print("\n  Moving motor {} from initial pos {} to final pos 0...".format(self.current_module_num, int(self.current_pos)), bash_colors.fg.red)
    try:
      self.arduino.calibrate_motor_pos(self.current_module_num, self.current_pos)
    except AttributeError:
      self.info("Not connected to an arduino")
    self.pretty_print("  Done", bash_colors.fg.red)
    self.verify_position()

  def verify_position(self):
    verify = self.pretty_input("\n  Is the shaft position of motor {} at 0? (Y/N) ".format(self.current_module_num), bash_colors.fg.purple)
    self.yes_no_response(verify, self.change_module, self.pos_input, self.verify_position)

  def change_module(self):
    change = self.pretty_input("\n  Do you want to change the position of another motor? (Y/N) ", bash_colors.fg.cyan)
    self.yes_no_response(change, self.module_num_input, self.close , self.change_module)

  def yes_no_response(self, response, yes_response, no_response, else_response):
    if response in ['Y', 'y']:
      yes_response()
    elif response in ['N', 'n']:
      no_response()
    else:
      self.pretty_print("  Response is not Y or N", bash_colors.fg.red)
      else_response()

  def close(self):
    self.arduino.close()
    sys.exit()

if __name__ == '__main__':
  MotorCalibration()

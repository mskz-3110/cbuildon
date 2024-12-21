from .tasks.init import *
from .tasks.build import *
from .tasks.test import *
from .tasks.valgrind import *

Task.parse_if_main(__name__, HelpTask())
def main():
  pass

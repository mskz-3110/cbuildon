from .tasks.init import *
from .tasks.android.build import *
from .tasks.windows.build import *
from .tasks.windows.test import *
from .tasks.valgrind.leak.check import *

Task.parse_if_main(__name__, HelpTask())
def main():
  pass

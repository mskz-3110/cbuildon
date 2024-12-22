from pyemon.task import *
from ....command import *
from ....platform import *
from ....test import *

class ValgrindLeakCheckTask(Task):
  def run(self, argv):
    valgrindArgs = [
      "valgrind",
      "--leak-check=full",
      "--show-leak-kinds=all",
    ] + argv
    platformName = platform_name()
    for testName in test_names():
      command(valgrindArgs + ["""./build/{}/bin/{}""".format(platformName, testName)])
if platform_name() != "windows":
  Task.parse_if_main(__name__, ValgrindLeakCheckTask("<valgrind options>"))

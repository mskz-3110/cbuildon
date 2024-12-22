from pyemon.task import *
from ...command import *
from ...platform import *
from ...test import *

class WindowsTestTask(Task):
  def run(self, argv):
    for buildDirectory in find("./build/windows/build/*/"):
      configuration = os.path.basename(os.path.dirname(buildDirectory)).split("_")[-1]
      for testName in test_names(argv):
        command(["""{}{}/{}.exe""".format(buildDirectory, configuration, testName)])
Task.parse_if_main(__name__, WindowsTestTask("<test names>"))

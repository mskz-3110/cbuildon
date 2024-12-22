from pyemon.task import *
from pyemon.status import *
from pyemon.path import *
from ..command import *
from ..platform import *
from ..cmake import *

class BuildWindowsTask(Task):
  def run(self, argv):
    if len(find("build/windows/build*.yaml")) == 0:
      fileStatus = FileStatus("build/windows/build_2022.yaml")
      if not fileStatus.exists():
        with open(fileStatus.Path, "w", newline = "\n") as file:
          file.write("""Visual Studio 17 2022:
  - Win32 MD Debug
  - Win32 MD Release
  - Win32 MT Debug
  - Win32 MT Release
  - x64 MD Debug
  - x64 MD Release
  - x64 MT Debug
  - x64 MT Release
""".format())
          fileStatus.done()
      print(fileStatus)

    if len(argv) == 0:
      paths = find("build/windows/build*.yaml")
    else:
      paths = argv
    for path in paths:
      cmake_build_windows(path)
Task.parse_if_main(__name__, BuildWindowsTask("<yaml file paths>"))

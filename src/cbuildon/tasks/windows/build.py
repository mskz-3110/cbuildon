from pyemon.task import *
from pyemon.status import *
from pyemon.path import *
from ...command import *
from ...platform import *
from ...cmake import *

class WindowsBuildTask(Task):
  def run(self, argv):
    prefix = "build/windows/build"
    buildFilePathPattern = """{}*.yaml""".format(prefix)
    if len(find(buildFilePathPattern)) == 0:
      fileStatus = FileStatus("""{}_2022.yaml""".format(buildFilePathPattern))
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
      paths = find(buildFilePathPattern)
    else:
      paths = argv
    for path in paths:
      cmake_build_windows(path)
Task.parse_if_main(__name__, WindowsBuildTask("<yaml file paths>"))

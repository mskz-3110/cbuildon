from .cmake import *
from .test import *

def windows_build(argv, isClean):
  oldDir = getdir()
  chdir("build/windows")
  pattern = "build*.yaml"
  if len(find(pattern)) == 0:
    filePath = """{}_2022.yaml""".format(pattern)
    if not exists(filePath):
      with open(filePath, "w", newline = "\n") as file:
        file.write('''Visual Studio 17 2022:
  - Win32 MD Debug
  - Win32 MD Release
  - Win32 MT Debug
  - Win32 MT Release
  - x64 MD Debug
  - x64 MD Release
  - x64 MT Debug
  - x64 MT Release
''')

  if len(argv) == 0:
    paths = find(pattern)
  else:
    paths = []
    for path in argv:
      paths.append(os.path.relpath("""{}/{}""".format(oldDir, path)))
  for path in paths:
    cmake_build_windows(path, isClean)
  chdir(oldDir)

def windows_test(argv):
  for buildDirectory in find("build/windows/build/*/"):
    configuration = os.path.basename(os.path.dirname(buildDirectory)).split("_")[-1]
    buildDirectory = buildDirectory.replace("\\", "/")
    for testName in test_names(argv):
      command(["""{}{}/{}.exe""".format(buildDirectory, configuration, testName)])

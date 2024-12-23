from .cmake import *
from .test import *

def android_build(argv, isClean):
  oldDir = getdir()
  chdir("build/android")
  pattern = "build*.yaml"
  if len(find(pattern)) == 0:
    filePath = """{}.yaml""".format(pattern)
    if not exists(filePath):
      with open(filePath, "w", newline = "\n") as file:
        file.write('''Ninja:
  - android-34 armeabi-v7a
  - android-34 arm64-v8a
''')

  androidNdkRoot = "../../../../ext/android"
  if len(argv) == 0:
    paths = find(pattern)
  else:
    paths = []
    for path in argv:
      paths.append(os.path.relpath("""{}/{}""".format(oldDir, path)))
  for path in paths:
    cmake_build_android(androidNdkRoot, path, isClean)
  chdir(oldDir)

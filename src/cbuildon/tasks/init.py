from pyemon.task import *
from pyemon.status import *
import os
from ..scripts.build.cbuildon_scripts.command import *

class InitTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("p", "project-name", "", "Project name")
    ])

  def copy(self, srcDir, dstDir, fileName):
    copy(os.path.join(srcDir, fileName), dstDir)
    print(FileStatus(os.path.relpath(os.path.join(dstDir, fileName)), "done"))

  def copy_if_not_exists(self, srcDir, dstDir, fileName):
    fileStatus = FileStatus(os.path.relpath(os.path.join(dstDir, fileName)))
    if copy_if_not_exists(os.path.join(srcDir, fileName), dstDir):
      fileStatus.done()
    print(fileStatus)

  def run(self, argv):
    self.OptionParser.parse(argv)

    srcRootDir = """{}/../scripts""".format(os.path.dirname(__file__))
    dstRootDir = "."

    for fileName in [".gitignore", "Dockerfile.debian"]:
      self.copy_if_not_exists(srcRootDir, dstRootDir, fileName)

    for fileName in ["cbuildon.py"]:
      self.copy(srcRootDir, dstRootDir, fileName)

    for dirName in ["build/cbuildon_scripts"]:
      dstDir = os.path.join(dstRootDir, dirName)
      rmkdir(dstDir)
      for srcPath in find("""{}/*.py""".format(os.path.join(srcRootDir, dirName))):
        self.copy(os.path.dirname(srcPath), dstDir, os.path.basename(srcPath))

    for filePath in ["build/common.cmake", "build/lib.cmake", "build/tests.cmake"]:
      dirName = os.path.dirname(filePath)
      self.copy_if_not_exists(os.path.join(srcRootDir, dirName), os.path.join(dstRootDir, dirName), os.path.basename(filePath))

    fileStatus = FileStatus(os.path.relpath(os.path.join(dstRootDir, "build/android/build.yaml")))
    if fileStatus.exists() is not True:
      mkdir(os.path.dirname(fileStatus.Path))
      with open(fileStatus.Path, "w", encoding = "utf-8", newline = "\n") as file:
        file.write('''Ninja:
  - android-34 armeabi-v7a Debug
  - android-34 armeabi-v7a Release
  - android-34 arm64-v8a Debug
  - android-34 arm64-v8a Release
''')
    print(fileStatus)

    fileStatus = FileStatus(os.path.relpath(os.path.join(dstRootDir, "build/ios/build.yaml")))
    if fileStatus.exists() is not True:
      mkdir(os.path.dirname(fileStatus.Path))
      with open(fileStatus.Path, "w", encoding = "utf-8", newline = "\n") as file:
        file.write('''Xcode:
  - arm64;arm64e Debug
  - arm64;arm64e Release
''')
    print(fileStatus)

    fileStatus = FileStatus(os.path.relpath(os.path.join(dstRootDir, "build/linux/build.yaml")))
    if fileStatus.exists() is not True:
      mkdir(os.path.dirname(fileStatus.Path))
      with open(fileStatus.Path, "w", encoding = "utf-8", newline = "\n") as file:
        file.write('''Debug:
Release:
''')
    print(fileStatus)

    fileStatus = FileStatus(os.path.relpath(os.path.join(dstRootDir, "build/macos/build.yaml")))
    if fileStatus.exists() is not True:
      mkdir(os.path.dirname(fileStatus.Path))
      with open(fileStatus.Path, "w", encoding = "utf-8", newline = "\n") as file:
        file.write('''Xcode:
  - x86_64;arm64 Debug
  - x86_64;arm64 Release
''')
    print(fileStatus)

    fileStatus = FileStatus(os.path.relpath(os.path.join(dstRootDir, "build/windows/build.yaml")))
    if fileStatus.exists() is not True:
      mkdir(os.path.dirname(fileStatus.Path))
      with open(fileStatus.Path, "w", encoding = "utf-8", newline = "\n") as file:
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
    print(fileStatus)

    projectName = self.OptionParser.find_option_from_long_name("project-name").Value
    if len(projectName) == 0:
      return

    for fileName in ["docker-compose.yaml"]:
      dst = os.path.join(dstRootDir, fileName)
      if exists(dst) is not True:
        with open(dst, "w", encoding = "utf-8", newline = "\n") as file:
          file.write(file_read(os.path.join(srcRootDir, fileName)).format(projectName = projectName))
        print(FileStatus(os.path.relpath(dst), "done"))

    for osName in ["ios", "macos", "windows", "android", "linux"]:
      dst = os.path.join(dstRootDir, """build/{}/lib/CMakeLists.txt""".format(osName))
      if exists(dst) is not True:
        mkdir(os.path.dirname(dst))
        with open(dst, "w", encoding = "utf-8", newline = "\n") as file:
          file.write("""cmake_minimum_required(VERSION 3.13)
project({projectName})
include(../../lib.cmake)
""".format(projectName = projectName))
        print(FileStatus(os.path.relpath(dst), "done"))

    for osName in ["macos", "windows", "linux"]:
      dst = os.path.join(dstRootDir, """build/{}/tests/CMakeLists.txt""".format(osName))
      if exists(dst) is not True:
        mkdir(os.path.dirname(dst))
        with open(dst, "w", encoding = "utf-8", newline = "\n") as file:
          file.write("""cmake_minimum_required(VERSION 3.13)
project({projectName})
include(../../tests.cmake)
""".format(projectName = projectName))
        print(FileStatus(os.path.relpath(dst), "done"))
Task.parse_if_main(__name__, InitTask())

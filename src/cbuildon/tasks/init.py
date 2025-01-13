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

  def run(self, argv):
    self.OptionParser.parse(argv)
    srcRootDir = os.path.abspath("""{}/../scripts""".format(os.path.dirname(__file__)))

    for dirName in ["inc", "src", "tests", "ext"]:
      mkdir(dirName)

    for baseName in [".gitignore", "Dockerfile.debian"]:
      self.copy_if_not_exists(srcRootDir, ".", baseName)

    for baseName in ["cbuildon.py"]:
      self.copy(srcRootDir, ".", baseName)

    dirName = "build/cbuildon_scripts"
    dstDir = dirName
    rmkdir(dstDir)
    for filePath in find("""{}/*.py""".format(os.path.join(srcRootDir, dirName))):
      self.copy(os.path.dirname(filePath), dstDir, os.path.basename(filePath))

    for osName in ["ios", "macos", "windows", "android", "linux"]:
      filePath = """build/{}/build.yaml""".format(osName)
      dirName = os.path.dirname(filePath)
      mkdir(dirName)
      self.copy_if_not_exists(os.path.join(srcRootDir, dirName), dirName, os.path.basename(filePath))

    projectName = self.OptionParser.find_option_from_long_name("project-name").Value
    if len(projectName) == 0:
      return

    project = {
      "projectName": projectName,
      "projectNamePrefix": projectName.upper(),
    }
    dirName = "build"
    dst = os.path.join(dirName, "project.json")
    status = Status(os.path.relpath(dst))
    if not exists(dst):
      json_save(dst, project)
      status.done()
    print(status)
    for baseName in ["common.cmake", "lib.cmake", "tests.cmake"]:
      dst = os.path.join(dirName, baseName)
      status = Status(os.path.relpath(dst))
      if not exists(dst):
        file_write(dst, file_read(os.path.join(srcRootDir, dst)).format(**project))
        status.done()
      print(status)

    baseName = "docker-compose.yaml"
    dst = baseName
    status = Status(os.path.relpath(dst))
    if not exists(dst):
      file_write(dst, file_read(os.path.join(srcRootDir, baseName)).format(projectName = projectName))
      status.done()
    print(status)

    for osName in ["ios", "macos", "windows", "android", "linux"]:
      dst = """build/{}/lib/CMakeLists.txt""".format(osName)
      status = Status(os.path.relpath(dst))
      if not exists(dst):
        mkdir(os.path.dirname(dst))
        file_write(dst, """cmake_minimum_required(VERSION 3.13)
project({projectName})
include(../../lib.cmake)
""".format(projectName = projectName))
        status.done()
      print(status)

    for osName in ["macos", "windows", "linux"]:
      dst = """build/{}/tests/CMakeLists.txt""".format(osName)
      status = Status(os.path.relpath(dst))
      if exists(dst) is not True:
        mkdir(os.path.dirname(dst))
        file_write(dst, """cmake_minimum_required(VERSION 3.13)
project({projectName})
include(../../tests.cmake)
""".format(projectName = projectName))
        status.done()
      print(status)
Task.parse_if_main(__name__, InitTask())

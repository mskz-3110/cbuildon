from pyemon.task import *
from pyemon.status import *
import os
from ..scripts.command import *

class InitTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("p", "project-name", "", "Project name")
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)

    for osName in ["windows", "linux", "android"]:
      osDirectory = """build/{}""".format(osName)
      mkdir(osDirectory)
      fileStatus = FileStatus("""{}/.gitignore""".format(osDirectory))
      if not fileStatus.exists():
        with open(fileStatus.Path, "w", newline = "\n") as file:
          file.write("/build")
          fileStatus.done()
      print(fileStatus)

    fileStatus = FileStatus("cbuildon.py", "done")
    with open(fileStatus.Path, "w", newline = "\n") as file:
      file.write('''import sys
import os
sys.path.append("""{}/build""".format(os.path.dirname(__file__)))
from cbuildon_scripts import *

chdir(os.path.dirname(__file__))
argv = sys.argv[1:]
taskName = shift(argv, "")
match taskName:
  case "windows.build":
    windows_build(argv, False)
  case "windows.rebuild":
    windows_build(argv, True)
  case "windows.test":
    windows_test(argv)
  case "android.build":
    android_build(argv, False)
  case "android.rebuild":
    android_build(argv, True)
  case "docker.build":
    command(["docker", "compose", "build"])
  case "docker.run":
    command(["docker", "compose", "run", "--rm", "debian", "bash"])
  case "linux.build":
    linux_build(False)
  case "linux.rebuild":
    linux_build(True)
  case "linux.test":
    linux_test(argv)
  case _:
    strings = []
    if 0 < len(taskName):
      strings.append("""\\033[40m\\033[31m{}\\033[0m is undefined.""".format(taskName))
    strings.append("""<Tasks>
  windows.build <yaml file paths>

  windows.rebuild <yaml file paths>

  windows.test <test names>

  android.build <yaml file paths>

  android.rebuild <yaml file paths>

  docker.build

  docker.run

  linux.build

  linux.rebuild

  linux.test <test names>
""")
    sys.exit("\\n".join(strings))
''')
    print(fileStatus)

    srcDirectory = """{}/../scripts""".format(os.path.dirname(__file__))
    dstDirectory = "build/cbuildon_scripts"
    rm(dstDirectory)
    mkdir(dstDirectory)
    for path in find("""{}/*.py""".format(srcDirectory)):
      fileName = os.path.basename(path)
      fileStatus = FileStatus("""{}/{}""".format(dstDirectory, fileName), "done")
      copy("""{}/{}""".format(srcDirectory, fileName), fileStatus.Path)
      print(fileStatus)

    projectName = self.OptionParser.find_option_from_long_name("project-name").Value
    if len(projectName) == 0:
      return

    fileStatus = FileStatus("""build/{}.cmake""".format(projectName))
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("""set(SRC_ROOT_PATH ${{PROJECT_ROOT_PATH}}/src)
set(SRCS)
list(APPEND SRCS ${{SRC_ROOT_PATH}}/{projectName}/{{SRC}}.c)

set(INCS)
list(APPEND INCS ${{PROJECT_ROOT_PATH}}/inc)
include_directories(${{INCS}})

add_library(${{PROJECT_NAME}}-Shared SHARED ${{SRCS}})
set_target_properties(${{PROJECT_NAME}}-Shared PROPERTIES OUTPUT_NAME ${{PROJECT_NAME}})
add_library(${{PROJECT_NAME}}-Static STATIC ${{SRCS}})
set_target_properties(${{PROJECT_NAME}}-Static PROPERTIES OUTPUT_NAME ${{PROJECT_NAME}})
""".format(projectName = projectName))
        fileStatus.done()
    print(fileStatus)

    fileStatus = FileStatus("build/windows/CMakeLists.txt")
    if not fileStatus.exists():
      with open(fileStatus.Path, "w", newline = "\n") as file:
        file.write("""cmake_minimum_required(VERSION 3.8)
project("{projectName}")
set(PROJECT_ROOT_PATH "../..")
set(CMAKE_CXX_FLAGS "${{CMAKE_CXX_FLAGS}} /source-charset:utf-8")
include(../${{PROJECT_NAME}}.cmake)
link_directories(${{CMAKE_BINARY_DIR}})
#target_link_libraries(${{PROJECT_NAME}}-Shared {{LIB}}.dll)
#target_link_libraries(${{PROJECT_NAME}}-Static {{LIB}}.lib)
set(TESTS_ROOT_PATH ${{PROJECT_ROOT_PATH}}/tests)
include_directories(${{TESTS_ROOT_PATH}})
set(TEST_NAMES)
list(APPEND TEST_NAMES test_test_{{SRC}})
foreach(testName IN LISTS TEST_NAMES)
  add_executable(${{testName}} ${{TESTS_ROOT_PATH}}/${{testName}}.c)
  target_link_libraries(${{testName}} ${{PROJECT_NAME}}.lib)
endforeach()
""".format(projectName = projectName))
        fileStatus.done()
    print(fileStatus)

    for osName in ["linux", "android"]:
      fileStatus = FileStatus("""build/{}/CMakeLists.txt""".format(osName))
      if not fileStatus.exists():
        with open(fileStatus.Path, "w", newline = "\n") as file:
          file.write("""cmake_minimum_required(VERSION 3.8)
project("{projectName}")
set(PROJECT_ROOT_PATH "../..")
include(../${{PROJECT_NAME}}.cmake)
link_directories(${{CMAKE_BINARY_DIR}})
#target_link_libraries(${{PROJECT_NAME}}-Shared {{LIB}}.so)
#target_link_libraries(${{PROJECT_NAME}}-Static {{LIB}}.a)
set(TESTS_ROOT_PATH ${{PROJECT_ROOT_PATH}}/tests)
include_directories(${{TESTS_ROOT_PATH}})
set(TEST_NAMES)
list(APPEND TEST_NAMES test_test_{{SRC}})
foreach(testName IN LISTS TEST_NAMES)
  add_executable(${{testName}} ${{TESTS_ROOT_PATH}}/${{testName}}.c)
  target_link_libraries(${{testName}} ${{PROJECT_NAME}}.a)
endforeach()
""".format(projectName = projectName))
          fileStatus.done()
      print(fileStatus)
Task.parse_if_main(__name__, InitTask())

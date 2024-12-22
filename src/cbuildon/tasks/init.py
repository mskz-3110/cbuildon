from pyemon.task import *
from pyemon.status import *
import os

class InitTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([
      Option("p", "project-name", "", "Project name")
    ])

  def run(self, argv):
    self.OptionParser.parse(argv)
    projectName = self.OptionParser.find_option_from_long_name("project-name").value_if_not(os.path.basename(os.getcwd()))

    for osName in ["windows", "android"]:
      directoryPath = """build/{}""".format(osName)
      os.makedirs(directoryPath, exist_ok = True)
      fileStatus = FileStatus("""{}/.gitignore""".format(directoryPath))
      if not fileStatus.exists():
        with open(fileStatus.Path, "w", newline = "\n") as file:
          file.write("/build")
          fileStatus.done()
      print(fileStatus)

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
set(CMAKE_CXX_FLAGS "/source-charset:utf-8")
include(../${{PROJECT_NAME}}.cmake)
link_directories(${{CMAKE_BINARY_DIR}})
#target_link_libraries(${{PROJECT_NAME}}-Shared {{LIB}}.dll)
#target_link_libraries(${{PROJECT_NAME}}-Static {{LIB}}.lib)
set(TESTS_ROOT_PATH ${{PROJECT_ROOT_PATH}}/tests)
include_directories(${{TESTS_ROOT_PATH}})
add_executable(test_{{SRC}} ${{TESTS_ROOT_PATH}}/test_{{SRC}}.c)
target_link_libraries(test_{{SRC}} ${{PROJECT_NAME}}.lib)
""".format(projectName = projectName))
        fileStatus.done()
    print(fileStatus)

    fileStatus = FileStatus("build/android/CMakeLists.txt")
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
add_executable(test_{{SRC}} ${{TESTS_ROOT_PATH}}/test_{{SRC}}.c)
target_link_libraries(test_{{SRC}} ${{PROJECT_NAME}}.a)
""".format(projectName = projectName))
        fileStatus.done()
    print(fileStatus)
Task.parse_if_main(__name__, InitTask())

from .cmake import *
from .test import *

def linux_build(isClean):
  oldDir = getdir()
  chdir("build/linux")
  cmake_build_linux(isClean)
  chdir(oldDir)

def linux_test(argv):
  for testName in test_names(argv):
    command(["valgrind", "--leak-check=full", "--show-leak-kinds=all", """./build/linux/build/{}""".format(testName)])

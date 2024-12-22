from .command import *
from pyemon.path import *

def test_names(testNames = []):
  if len(testNames) == 0:
    return list(map(lambda filePath: Path.from_file_path(filePath).File, find("tests/*.c") + find("tests/*.cpp")))
  else:
    return testNames

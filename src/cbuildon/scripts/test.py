from .command import *

def test_names(testNames = []):
  if len(testNames) == 0:
    return list(map(lambda filePath: os.path.splitext(os.path.basename(filePath))[0], find("tests/*.c") + find("tests/*.cpp")))
  else:
    return testNames

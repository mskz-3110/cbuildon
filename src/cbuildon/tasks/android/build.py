from pyemon.task import *
from pyemon.status import *
from pyemon.path import *
from ...command import *
from ...platform import *
from ...cmake import *

class AndroidBuildTask(Task):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.OptionParser = OptionParser([Option("n", "android-ndk-root", "./ext/android", "Android NDK Root path")])

  def run(self, argv):
    self.OptionParser.parse(argv)
    prefix = "build/android/build"
    buildFilePathPattern = """{}*.yaml""".format(prefix)
    if len(find(buildFilePathPattern)) == 0:
      fileStatus = FileStatus("""{}.yaml""".format(prefix))
      if not fileStatus.exists():
        with open(fileStatus.Path, "w", newline = "\n") as file:
          file.write("""Ninja:
  - android-34 armeabi-v7a
  - android-34 arm64-v8a
""".format())
          fileStatus.done()
      print(fileStatus)

    androidNdkRoot = """../../{}""".format(os.path.relpath(self.OptionParser.find_option_from_long_name("android-ndk-root").Value).replace(os.sep, "/"))
    if len(self.OptionParser.Argv) == 0:
      paths = find(buildFilePathPattern)
    else:
      paths = self.OptionParser.Argv
    for path in paths:
      cmake_build_android(androidNdkRoot, path)
Task.parse_if_main(__name__, AndroidBuildTask("<yaml file paths>"))

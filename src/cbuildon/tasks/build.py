from pyemon.task import *
from pyemon.status import *
from pyemon.path import *
from ..command import *
import platform
import yaml
import os

class BuildTask(Task):
  def run(self, argv):
    match platform.system():
      case "Windows":
        os.chdir("build/windows")
        fileStatus = FileStatus("build.yaml")
        if not fileStatus.exists():
          with open(fileStatus.Path, "w", newline = "\n") as file:
            file.write("""Generators:
  Visual Studio 17 2022:
    - Win32 MD Debug
    - Win32 MD Release
    - Win32 MT Debug
    - Win32 MT Release
    - x64 MD Debug
    - x64 MD Release
    - x64 MT Debug
    - x64 MT Release
""".format())
            fileStatus.done()
        print(fileStatus)

        Path.from_file_path("build").makedirs()
        with open(fileStatus.Path, "r", encoding = "utf-8") as file:
          buildConfig = yaml.safe_load(file)
          if "Generators" in buildConfig:
            for generator in buildConfig["Generators"].keys():
              version = generator.split(" ")[-1]
              for combination in buildConfig["Generators"][generator]:
                arch, runtime, config = combination.split(" ")
                directory = """build/{}""".format("_".join([version, arch, runtime, config]))
                if Path.from_file_path(directory).exists() is False:
                  # cmake -G "Visual Studio 17 2022" -A x64 -D CMAKE_MSVC_RUNTIME_LIBRARY=MultiThreadedDebug -B build/2022_x64_MT_Debug
                  msvcRuntimeLibrary = "MultiThreaded"
                  if config == "Debug":
                    msvcRuntimeLibrary += config
                  if runtime == "MD":
                    msvcRuntimeLibrary += "DLL"
                  command([
                    "cmake",
                    "-G", generator,
                    "-A", arch,
                    "-D", """CMAKE_MSVC_RUNTIME_LIBRARY={}""".format(msvcRuntimeLibrary),
                    "-B", directory,
                  ])
                command([
                  "cmake",
                  "--build", directory,
                  "--config", config,
                ])
Task.parse_if_main(__name__, BuildTask())

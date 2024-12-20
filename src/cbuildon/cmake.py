import os
import yaml
from .command import *
from .platform import *

def cmake_msvc_runtime_library(runtime, configuration):
  msvcRuntimeLibrary = "MultiThreaded"
  if configuration == "Debug":
    msvcRuntimeLibrary += configuration
  if runtime == "MD":
    msvcRuntimeLibrary += "DLL"
  return msvcRuntimeLibrary

def cmake_build(filePath):
  if os.path.isfile(filePath) is False:
    sys.exit("""{} does not exist.""".format(Command.to_error_string(filePath)))
  with open(filePath, "r", encoding = "utf-8") as file:
    buildConfig = yaml.safe_load(file)
    os.chdir(os.path.dirname(filePath))
    match platform_name():
      case "windows":
        for generator in buildConfig.keys():
          version = generator.split(" ")[-1]
          for combination in buildConfig[generator]:
            arch, runtime, configuration = combination.split(" ")
            buildDirectory = """build/{}""".format("_".join([version, arch, runtime, configuration]))
            if os.path.isdir(buildDirectory) is False:
              mkdir("build")
              command([
                "cmake",
                "-G", generator,
                "-A", arch,
                "-D", """CMAKE_MSVC_RUNTIME_LIBRARY={}""".format(cmake_msvc_runtime_library(runtime, configuration)),
                "-B", buildDirectory,
              ])
            command([
              "cmake",
              "--build", buildDirectory,
              "--config", configuration,
            ])

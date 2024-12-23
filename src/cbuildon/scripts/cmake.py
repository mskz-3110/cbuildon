import os
import yaml
from .command import *
from .platform import *

def cmake_build_android(androidNdkRoot, filePath, isClean):
  exists_assert(filePath)
  with open(filePath, "r", encoding = "utf-8") as file:
    buildConfig = yaml.safe_load(file)
    for generator in buildConfig.keys():
      for combination in buildConfig[generator]:
        platform, abi = combination.split(" ")
        buildDirectory = """build/{}""".format("_".join([platform, abi]))
        if os.path.isdir(buildDirectory) is False:
          mkdir("build")
          command([
            "cmake",
            "-G", generator,
            "-D", """CMAKE_TOOLCHAIN_FILE={}/build/cmake/android.toolchain.cmake""".format(androidNdkRoot),
            "-D", """ANDROID_PLATFORM={}""".format(platform),
            "-D", """ANDROID_ABI={}""".format(abi),
            "-B", buildDirectory,
          ])
        elif isClean:
          command([
            "cmake",
            "--build", buildDirectory,
            "--target", "clean",
          ])
        command([
          "cmake",
          "--build", buildDirectory,
        ])

def cmake_msvc_runtime_library(runtime, configuration):
  msvcRuntimeLibrary = "MultiThreaded"
  if configuration == "Debug":
    msvcRuntimeLibrary += configuration
  if runtime == "MD":
    msvcRuntimeLibrary += "DLL"
  return msvcRuntimeLibrary

def cmake_build_windows(filePath, isClean):
  exists_assert(filePath)
  with open(filePath, "r", encoding = "utf-8") as file:
    buildConfig = yaml.safe_load(file)
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
        elif isClean:
          command([
            "cmake",
            "--build", buildDirectory,
            "--config", configuration,
            "--target", "clean",
          ])
        command([
          "cmake",
          "--build", buildDirectory,
          "--config", configuration,
        ])

def cmake_build_linux(isClean):
  if os.path.isdir("build") is False:
    mkdir("build")
    command([
      "cmake",
      "-B", "build",
    ])
  elif isClean:
    command([
      "cmake",
      "--build", "build",
      "--target", "clean",
    ])
  command([
    "cmake",
    "--build", "build"
  ])

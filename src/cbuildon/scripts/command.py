import subprocess
import datetime as dt
import sys
import os
import glob
import shutil

def command(args, onProcess = None):
  if onProcess is None:
    onProcess = lambda result: """\033[40m\033[31mFail: Return code is {}.\033[0m""".format(result.returncode)
  print("""\033[40m\033[32m[{}] {} $ {}\033[0m""".format(dt.datetime.now().strftime("%y/%m/%d %H:%M:%S"), os.getcwd(), " ".join(args)))
  result = subprocess.run(args)
  if result.returncode != 0:
    exitArg = onProcess(result)
    if exitArg is not None:
      sys.exit(exitArg)
  return result

def copy(src, dst):
  if os.path.isfile(src):
    shutil.copy2(src, dst)
  else:
    shutil.copytree(src, dst)

def rm(path):
  if os.path.exists(path):
    shutil.rmtree(path)

def mkdir(path):
  os.makedirs(path, exist_ok = True)

def rmkdir(path):
  rm(path)
  mkdir(path)

def chdir(path):
  os.chdir(path)

def getdir():
  return os.getcwd()

def find(pattern, recursive = True):
  paths = []
  for path in glob.glob(pattern, recursive = recursive):
    paths.append(path)
  return paths

def exists(path):
  return os.path.exists(path)

def exists_assert(path):
  if exists(path) is False:
    sys.exit("""\033[40m\033[31m{}\033[0m does not exist.""".format(path))

def shift(array, defaultValue = None):
  if 0 < len(array):
    return array.pop(0)
  return defaultValue

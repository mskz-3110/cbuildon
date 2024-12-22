from pyemon.command import *
import sys
import os
import glob
import shutil

def command(args, onProcess = None):
  if onProcess is None:
    onProcess = lambda result: """Fail: Return code is {}.""".format(result.returncode)
  result = Command(args).run()
  if result.returncode != 0:
    exitArg = onProcess(result)
    if exitArg is not None:
      sys.exit(exitArg)
  return result

def mkdir(path, onBlock = None):
  os.makedirs(path, exist_ok = True)
  if onBlock is not None:
    onBlock()

def chdir(path, onBlock = None):
  if onBlock is None:
    os.chdir(path)
  else:
    backupPath = os.getcwd()
    os.chdir(path)
    onBlock()
    os.chdir(backupPath)

def rmdir(path):
  shutil.rmtree(path)

def find(pattern, recursive = True):
  paths = []
  for path in glob.glob(pattern, recursive = recursive):
    paths.append(path)
  return paths

def file_exists_assert(filePath):
  if os.path.isfile(filePath) is False:
    sys.exit("""{} does not exist.""".format(Command.to_error_string(filePath)))

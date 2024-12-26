import subprocess
import datetime
import sys
import os
import glob
import shutil
import yaml

def color_to_escape(color):
  match color:
    case "black":
      return 0
    case "red":
      return 1
    case "green":
      return 2
    case "yellow":
      return 3
    case "blue":
      return 4
    case "magenta":
      return 5
    case "cyan":
      return 6
    case "gray":
      return 7
    case _:
      return 9

def console_string(value, fgColor, bgColor = "black"):
  return """\033[{}m\033[{}m{}\033[0m""".format(color_to_escape(bgColor) + 40, color_to_escape(fgColor) + 30, value)

def command(args, onProcess = None, **kwargs):
  if onProcess is None:
    onProcess = lambda result: console_string("""Fail: Return code is {}.""".format(result.returncode), "red")
  commandString = args
  if type(args) is not str:
    commandString = " ".join(args)
  print(console_string("""[{}] {} $ {}""".format(datetime.datetime.now().strftime("%y/%m/%d %H:%M:%S"), os.getcwd(), commandString), "green"))
  result = subprocess.run(args, **kwargs)
  if result.returncode != 0:
    exitArg = onProcess(result)
    if exitArg is not None:
      sys.exit(exitArg)
  return result

def capture_command(args, onProcess = None, **kwargs):
  return command(args, onProcess, **(dict(capture_output = True, text = True, encoding = "utf-8") | kwargs))

def exists(path):
  return os.path.exists(path)

def exists_assert(path):
  if exists(path) is False:
    sys.exit("""{} does not exist.""".format(console_string(path, "red")))

def copy(src, dst):
  if os.path.isfile(src):
    shutil.copy2(src, dst)
  else:
    shutil.copytree(src, dst)

def copy_if_not_exists(src, dst):
  if not os.path.exists(os.path.join(dst, os.path.basename(src))):
    copy(src, dst)
    return True
  return False

def rm(path):
  if os.path.isfile(path):
    os.remove(path)
  elif os.path.isdir(path):
    shutil.rmtree(path)

def move(src, dst):
  rm(os.path.join(dst, os.path.basename(src)))
  shutil.move(src, dst)

def mkdir(path):
  if 0 < len(path):
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

def shift(array, defaultValue = None):
  if 0 < len(array):
    return array.pop(0)
  return defaultValue

def yaml_load(filePath):
  with open(filePath, "r", encoding = "utf-8") as file:
    return yaml.safe_load(file)
  return {}

def yaml_save(filePath, data):
  mkdir(os.path.dirname(filePath))
  with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
    yaml.dump(data, file, sort_keys = False, default_flow_style = False, allow_unicode = True)

def file_read(filePath):
  with open(filePath, "r", encoding = "utf-8") as file:
    return file.read()
  return ""

def file_write(filePath, data):
  mkdir(os.path.dirname(filePath))
  with open(filePath, "w", encoding = "utf-8", newline = "\n") as file:
    file.write(data)

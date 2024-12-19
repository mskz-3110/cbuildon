from pyemon.command import *
import sys

def command(args, onProcess = None):
  if onProcess is None:
    onProcess = lambda result: """Fail: Return code is {}.""".format(result.returncode)
  result = Command(args).run()
  if result.returncode != 0:
    exitArg = onProcess(result)
    if exitArg is not None:
      sys.exit(exitArg)
  return result

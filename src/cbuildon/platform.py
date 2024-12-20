import platform

def platform_name():
  platformName = platform.system().lower()
  if len(platformName) == 0:
    platformName = "unknown"
  return platformName

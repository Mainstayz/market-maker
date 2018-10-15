import subprocess
# Constants
XBt_TO_XBT = 100000000
VERSION = 'v1.1'


retcode = subprocess.call(["ls", "-l"])
print(retcode)

try:
    VERSION = str(subprocess.check_output(["git", "describe", "--tags"], stderr=subprocess.DEVNULL).rstrip())
    print(VERSION)
except Exception as e:
    # git not available, ignore
    pass

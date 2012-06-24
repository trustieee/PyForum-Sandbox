# pageping.py

from subprocess import Popen, PIPE # for executing a process (in our case, ping.exe)
import re # for matching the packets lost in a ping command
import time
import sys

debug = True # toggle this to false if this is running in a production environment

page = sys.argv[1]
n = 1
sleepTime = 60 # seconds

if debug:
    sleepTime = 5 # seconds

# 1) need a loop that only iterates every 600 seconds, 10 minutes
while True:
    #ping 'page' 'n' times
    p = Popen("ping.exe {0} -n {1}".format(page, n), stderr=PIPE, stdout=PIPE)

    # store stdout/stderr results in tuple
    (out, err) = p.communicate()

    # find packets lost (typically either 0 or 100) and store the number in the first (and only) group (m.group(1))
    m = re.search("\((\d+)\% loss\)", out)
    print m.group(1) #typically yields either 0 or 100

    time.sleep(sleepTime)



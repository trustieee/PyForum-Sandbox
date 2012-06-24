# Script: pageping.py
# Purpose: Continually checks the status of a given URL.

from subprocess import Popen, PIPE # for executing a process (in our case, ping.exe)
import re # for matching the packets lost in a ping command
from time import sleep
import sys

DEBUG = True # toggle this to false if this is running in a production environment

try:
    page = sys.argv[1]
except IndexError:
    page = 'google.com'

PING_COUNT = 1
SLEEP_TIME = 60 # seconds

if DEBUG:
    SLEEP_TIME = 5 # seconds

# 1) need a loop that only iterates every 600 seconds, 10 minutes
while True:
    # ping 'page' 'n' times
    p = Popen("ping.exe {0} -n {1}".format(page, PING_COUNT), stderr=PIPE, stdout=PIPE)

    # store stdout/stderr results in tuple
    (out, err) = p.communicate()

    # find packets lost (typically either 0 or 100) and store the number in the first (and only) group (m.group(1))
    m = re.search("\((\d+)\% loss\)", out)
    print m.group(1) # typically yields either 0 or 100

    sleep(SLEEP_TIME)



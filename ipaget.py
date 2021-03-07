# Python3 IPA Getter
# Requires Frida and port 22 SSH on iOS device
# Check frida-ios-dump's pip requirements too

from os import path
from platform import machine
from signal import signal, SIGINT
from subprocess import Popen, run, PIPE
import sys
from getopt import getopt, GetoptError

interpreter = sys.executable
ipadir = path.dirname(path.realpath(__file__)) + '/ipas/'
opts = None

try:
    opts, args = getopt(sys.argv[1:], 'hlwi:')
except GetoptError:
    print('For help: ipaget.py -h')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-h':
        print(
            '\nUsage: ipaget.py [options]\n'
            'This script interactively helps you extract your own IPA files.\n'
            'Check the frida-ios-dump folder for more information.\n'
            'Obviously, you must have the app installed to create an IPA.\n'
            "Enter either 'list' or [bundleid] when prompted to extract IPAs.\n\n"
            '  -h           this help\n')
        sys.exit()

if machine() != 'x86_64':
    exit('You need to run a x86_64 Python binary! Use Rosetta 2 and a x86_64 Python binary!')

iproxy = Popen(['iproxy', '2222', '22'], stdout=PIPE)


def signal_handler(signal, frame):
    Popen.kill(iproxy)
    sys.exit(0)


signal(SIGINT, signal_handler)

done = False
while not done:
    target = input("Enter Target App ID, type 'list' to list apps: ")
    if target == 'list':
        run([interpreter, 'frida-ios-dump/dump.py', '-l'])
    else:
        run([interpreter, 'frida-ios-dump/dump.py', str(target), '-o', ipadir + str(target)])
        done = True

Popen.kill(iproxy)
sys.exit()

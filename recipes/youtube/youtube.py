#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
from getopt import getopt, GetoptError
import subprocess
from sys import argv
from warnings import simplefilter
from debian import deb822
from requests import get
import shutil
import os
import patoolib
import sys
sys.path.append('../../')
from libbakery import fetchdylib, headers

LocalDylibs = False
ipa_path = 'com.google.ios.youtube.ipa'
opts = None

simplefilter('ignore', lineno=740)

try:
    opts, args = getopt(argv[1:], 'hli:')
except GetoptError:
    print('For help: youtube.py -h')
    exit(2)

for opt, arg in opts:
    if opt == '-h':
        print(
            '\nUsage: youtube.py [options]\n'
            'This script expects ' + ipa_path +
            ' to be present in the root folder of this recipe.\n'
            'It must be a YouTube IPA, and it should be extracted from your own device.\n'
            'You can also specify a custom path to the IPA.\n\n'
            '  -h           this help\n'
            '  -l           use local already-downloaded dylibs\n'
            '  -i [path]    specify path to ipa\n')
        exit()
    elif opt == '-l':
        LocalDylibs = True
        print('INFO: force use local dylibs')
    elif opt == '-i':
        ipa_path = arg


if not LocalDylibs:
    print('Getting latest dylibs...')
    raw_packages = get('https://apt.alfhaily.me/Packages',
                       headers=headers).content
    KeepFiles = True
    fetchdylib('https://apt.alfhaily.me/', 'me.alfhaily.cercube',
               'Cercube.dylib', raw_packages, True)
    os.rename('tmp/Cercube', 'Cercube')
    shutil.rmtree('tmp')
    if not os.path.isdir('Resources'):
        os.mkdir('Resources')
    if os.path.isdir('Resources/Cercube.bundle'):
        print('Deleting previous Cercube bundle for upgrade')
        shutil.rmtree('Resources/Cercube.bundle')
    shutil.move('Cercube/Library/Application Support/Cercube/Cercube.bundle',
                'Resources/Cercube.bundle')
    shutil.rmtree('Cercube')
    print('Saved Cercube.bundle successfully.')


print('\nBaking IPA.')
subprocess.run(['make', 'clean', 'all', 'package',
               'FINALPACKAGE=1', 'CODESIGN_IPA=0', '-w'])
print('\nDone. IPA is in packages folder.')

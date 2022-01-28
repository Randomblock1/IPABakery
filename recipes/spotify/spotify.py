#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
import libbakery
from getopt import getopt, GetoptError
from subprocess import run
from sys import argv
from warnings import simplefilter
import sys
sys.path.append('../../')

LocalDylibs = False
ipa_path = 'com.spotify.client.ipa'
opts = None

simplefilter('ignore', lineno=740)

try:
    opts, args = getopt(argv[1:], 'hlwi:')
except GetoptError:
    print('For help: spotify.py -h')
    exit(2)

for opt, arg in opts:
    if opt == '-h':
        print(
            '\nUsage: spotify.py [options]\n'
            'This script expects ' + ipa_path +
            ' to be present in the root folder of this recipe.\n'
            'It must be a Spotify IPA, and it should be extracted from your own device.\n'
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
    packages = libbakery.fetchpackages('https://repo.dynastic.co/')
    libbakery.fetchdylib('https://repo.dynastic.co/', 'com.spos',
                         'Sposify.dylib', packages)

    packages = libbakery.fetchpackages(
        'https://julio.hackyouriphone.org/Packages')
    libbakery.fetchdylib('https://julio.hackyouriphone.org/',
                         'com.julioverne.spotilife', 'Spotilife.dylib', packages)
    print('All dylibs successfully fetched.')


print('\nBaking IPA.')
run(['make', 'clean', 'all', 'package', 'FINALPACKAGE=1', 'CODESIGN_IPA=0'])
print('\nDone. IPA is in packages folder.')

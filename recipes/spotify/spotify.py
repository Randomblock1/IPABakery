#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
import os
from bz2 import decompress
from getopt import getopt, GetoptError
from shutil import rmtree
from subprocess import run
from sys import argv
from warnings import simplefilter
from zipfile import ZipFile
from debian import deb822
from requests import get
import patoolib
import shutil

LocalDylibs = False
KeepWatchApp = False
ipa_path = 'com.spotify.client.ipa'
opts = None
KeepFiles = False

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
            "  -w           keep watch app extension (you'll have to sign all app extensions for it to work)\n"
            '  -i [path]    specify path to ipa\n')
        exit()
    elif opt == '-l':
        LocalDylibs = True
        print('INFO: force use local dylibs')
    elif opt == '-w':
        KeepWatchApp = True
        print('INFO: keep watch app')
    elif opt == '-i':
        ipa_path = arg

headers = {
    'X-Machine': 'iPhone6,1',
    'X-Unique-ID': '8843d7f92416211de9ebb963ff4ce28125932878',
    'X-Firmware': '10.1.1',
    'User-Agent': 'Telesphoreo APT-HTTP/1.0.592',
    'Accept-Language': 'en-US,*',
}


def fetchdylib(repo, package_id, dylib, packages):
    prev_version = '0'
    for src in deb822.Sources.iter_paragraphs(packages):
        if src['Package'] == str(package_id):
            package_url = src['Filename']
            if src['Version'] > prev_version:
                new_version = src['Version']
                if prev_version != '0':
                    print('Updating ' + dylib + ' from ' +
                          prev_version + ' to ' + new_version)
                prev_version = new_version
                with get(repo + str(package_url), headers=headers, allow_redirects=True) as raw_deb:
                    open('temp.deb', 'wb').write(raw_deb.content)
                    patoolib.extract_archive('temp.deb', outdir='tmp')
                    os.rename(
                        'tmp/Library/MobileSubstrate/DynamicLibraries/' + dylib, dylib)
                    os.remove('temp.deb')
                    print('Saved ' + str(dylib) + ' successfully.')
                    if KeepFiles == False:
                        shutil.rmtree('tmp')


if not LocalDylibs:
    print('Getting latest dylibs...')
    raw_packages = decompress(
        get('https://repo.dynastic.co/Packages.bz2', headers=headers).content)
    fetchdylib('https://repo.dynastic.co/', 'com.spos',
               'Sposify.dylib', raw_packages)

    raw_packages = get(
        'https://julio.hackyouriphone.org/Packages', headers=headers).content
    fetchdylib('https://julio.hackyouriphone.org/',
               'com.julioverne.spotilife', 'Spotilife.dylib', raw_packages)
    print('All dylibs successfully fetched.')


print('\nBaking IPA.')
run(['make', 'clean', 'all', 'package', 'FINALPACKAGE=1', 'CODESIGN_IPA=0'])
print('\nDone. IPA is in packages folder.')

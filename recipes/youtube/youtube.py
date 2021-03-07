#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
from getopt import getopt, GetoptError
from io import BytesIO
import subprocess
from sys import argv
from warnings import simplefilter
from debian import deb822
from debian import debfile
from requests import get
import shutil
import os

LocalDylibs = False
KeepWatchApp = False
ipa_path = 'com.google.ios.youtube.ipa'
opts = None
GlobalDeb = False

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
            'This script expects ' + ipa_path + ' to be present in the root folder of this recipe.\n'
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
                    print('Updating ' + dylib + ' from ' + prev_version + ' to ' + new_version)
                prev_version = new_version
                with get(repo + str(package_url), headers=headers, allow_redirects=True) as raw_deb:
                    if GlobalDeb:
                        global deb
                    deb = debfile.DebFile(fileobj=BytesIO(raw_deb.content))
                    open(dylib, 'wb').write(deb.data.get_content('Library/MobileSubstrate/DynamicLibraries/' + dylib))
                    print('Saved ' + str(dylib) + ' successfully.')


if not LocalDylibs:
    print('Getting latest dylibs...')
    raw_packages = get('https://apt.alfhaily.me/Packages', headers=headers).content
    fetchdylib('https://apt.alfhaily.me/', 'me.alfhaily.cercube', 'Cercube.dylib', raw_packages)
    GlobalDeb = True
    deb.data.tgz().extractall('Cercube')
    if not os.path.isdir('Resources'):
        os.mkdir('Resources')
    if os.path.isdir('Resources/Cercube.bundle'):
        print('Deleting previous Cercube bundle for upgrade')
        shutil.rmtree('Resources/Cercube.bundle')
    shutil.move('Cercube/Library/Application Support/Cercube/Cercube.bundle', 'Resources/Cercube.bundle')
    shutil.rmtree('Cercube')
    print('Saved Cercube.bundle successfully.')
    GlobalDeb = False


print('\nBaking IPA.')
subprocess.run(['make', 'clean', 'all', 'package', 'FINALPACKAGE=1', 'CODESIGN_IPA=0', '-w'])
print('\nDone. IPA is in packages folder.')

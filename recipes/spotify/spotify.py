#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
import os
from bz2 import decompress
from getopt import getopt, GetoptError
from io import BytesIO
from shutil import rmtree
from subprocess import run
from sys import argv
from warnings import simplefilter
from zipfile import ZipFile
from debian import deb822
from debian import debfile
from requests import get

LocalDylibs = False
KeepWatchApp = False
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
            'This script expects ' + ipa_path + ' to be present in the root folder of this recipe.\n'
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
    for src in deb822.Sources.iter_paragraphs(packages):
        if src['Package'] == str(package_id):
            package_url = src['Filename']
            with get(repo + str(package_url), headers=headers, allow_redirects=True) as raw_deb:
                deb = debfile.DebFile(fileobj=BytesIO(raw_deb.content))
                open(dylib, 'wb').write(deb.data.get_content('Library/MobileSubstrate/DynamicLibraries/' + dylib))
                print('Saved ' + str(dylib) + ' successfully.')


if not LocalDylibs:
    print('Getting latest dylibs...')
    raw_packages = decompress(get('https://repo.dynastic.co/Packages.bz2', headers=headers).content)
    fetchdylib('https://repo.dynastic.co/', 'com.spos', 'Sposify.dylib', raw_packages)

    raw_packages = get('https://julio.hackyouriphone.org/Packages', headers=headers).content
    fetchdylib('https://julio.hackyouriphone.org/', 'com.julioverne.spotilife', 'Spotilife.dylib', raw_packages)
    print('All dylibs successfully fetched.')

print('\n')

try:
    with ZipFile(ipa_path, 'r') as ipa:
        try:
            ipa.extractall()
            if not KeepWatchApp:
                ipa.read('Payload/Spotify.app/com.apple.WatchPlaceholder/')
                print('Need to remove WatchApp so AltStore can sign it without app extensions')
                rmtree('Payload/Spotify.app/com.apple.WatchPlaceholder/')
                with ZipFile('fixed.' + ipa_path, 'w') as fixed_ipa:
                    for dirname, subdirs, files in os.walk('Payload'):
                        fixed_ipa.write(dirname)
                        for filename in files:
                            fixed_ipa.write(os.path.join(dirname, filename))
                print('Removed watch app')
            else:
                print('Skipping watch app removal')
        except KeyError:
            print('IPA already removed watch app')
        rmtree('Payload')
        ipa.close()
    if os.path.exists('fixed.' + ipa_path):
        os.remove(ipa_path)
        os.rename('fixed.' + ipa_path, ipa_path)
except FileNotFoundError:
    print('com.spotify.client.ipa not found.')

print('\nBaking IPA.')
run(['make', 'clean', 'all', 'package', 'FINALPACKAGE=1', 'CODESIGN_IPA=0'])
print('\nDone. IPA is in packages folder.')

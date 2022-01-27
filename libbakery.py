from contextlib import nullcontext
from getopt import GetoptError
import os
import shutil
from debian import deb822
from requests import get, HTTPError
import patoolib

headers = {
    'X-Machine': 'iPhone6,1',
    'X-Unique-ID': '8843d7f92416211de9ebb963ff4ce28125932878',
    'X-Firmware': '10.1.1',
    'User-Agent': 'Telesphoreo APT-HTTP/1.0.592',
    'Accept-Language': 'en-US,*',
}

def fetchrepo(repo):
    compressions = ['', '.xz', '.gz', '.bz2', '.lzma']
    for extension in compressions:
        try:
            result = get(repo + '/Packages' + extension, headers=headers)
            result.raise_for_status()
            break
        except HTTPError:
            continue
    return result.content

def fetchdylib(repo, package_id, dylib, packages, keepfiles=False):
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
                    if not keepfiles:
                        shutil.rmtree('tmp')
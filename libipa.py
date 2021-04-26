#!/usr/bin/python3
# libIPA contains functions for manipulating IPAs and DEBs
import bz2
from io import BytesIO
from debian import deb822
from debian import debfile
from requests import get

http_headers = {
    'X-Machine': 'iPhone6,1',
    'X-Unique-ID': '8843d7f92416211de9ebb963ff4ce28125932878',
    'X-Firmware': '10.1.1',
    'User-Agent': 'Telesphoreo APT-HTTP/1.0.592',
    'Accept-Language': 'en-US,*',
}


def fetchpackages(repo, decompress=None):
    raw_repo = get(repo, headers=http_headers)
    if decompress is None:
        return raw_repo.content
    else:
        if decompress == 'bz2':
            return bz2.decompress(raw_repo.content)
        else:
            exit("Unknown compression method")


def fetchdylib(repo, package_id, dylib, packages, returndeb=False):
    prev_version = '0'
    for src in deb822.Sources.iter_paragraphs(packages):
        if src['Package'] == str(package_id):
            package_url = src['Filename']
            if src['Version'] > prev_version:
                new_version = src['Version']
                if prev_version != '0':
                    print('Updating ' + dylib + ' from ' + prev_version + ' to ' + new_version)
                prev_version = new_version
                with get(repo + str(package_url), headers=http_headers, allow_redirects=True) as raw_deb:
                    deb = debfile.DebFile(fileobj=BytesIO(raw_deb.content))
                    open(dylib, 'wb').write(deb.data.get_content('Library/MobileSubstrate/DynamicLibraries/' + dylib))
                    print('Saved ' + str(dylib) + ' successfully.')
                    if returndeb:
                        return deb


def makerecipe(path):
    #todo
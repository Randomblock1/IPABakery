# IPABakery
is a collection of Python scripts to automate generating tweaked IPAs from normal apps.

## READ
I no longer have time to work on this, so I'm posting the source code as-is. It works, mostly, and the code is not what I would call best practices. Feel free to fork it and submit a PR.

## Requirements
You need:
- [Theos and Theos Jailed](https://github.com/kabiroberai/theos-jailed/wiki/Installation)
- Python3 and pip
If you are going to obtain your own IPA files:
- iproxy (comes with usbmuxd on Linux)
- A jailbroken device with [Frida](https://frida.re/docs/ios/#with-jailbreak) installed

## Setup
- `git clone --recursive https://github.com/randomblock1/IPABakery` (`--recursive` makes sure the submodule is ready!)
- `python3 -m pip install -r requirements.txt`
- `python3 -m pip install -r frida-ios-dump/requirements.txt`

## Usage
`ipaget.py` is a simple wrapper for Frida-iOS-Dump that automatically starts and stops iproxy and interactively selects apps to dump.

If you don't intend to dump your own IPAs, you can skip `ipaget.py` and move on to making recipes.

Within the recipes folder, I've made Theos Jailed projects with python scripts that automatically download the latest .deb files
and extracts the neccessary files. It then builds a tweaked IPA using the tweaks and IPAs you fed it.
Just run `python3 [script] -h` for help.

It's highly recommended to use [this fork](https://github.com/kabiroberai/theos-jailed/pull/71) 
of theos-jailed, for Substitute (A12) support.

TODO: minimize duplicate code (this is my first python program i know its bad)

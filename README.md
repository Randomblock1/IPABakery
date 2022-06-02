# IPABakery

is a collection of Python scripts to automate generating tweaked IPAs from normal apps.

## Requirements

You need:

- [Theos and Theos Jailed](https://github.com/kabiroberai/theos-jailed/wiki/Installation)
- Python3 and pip

  If you are going to obtain your own IPA files:
- [ipatool](https://github.com/majd/ipatool)

## Setup

- `git clone https://github.com/randomblock1/IPABakery`
- `python3 -m pip install -r requirements.txt`

## Usage

Use [ipatool](https://github.com/majd/ipatool) to download IPA files using your Apple ID. No jailbroken device required. (You have to "purchase" it in the App Store before being able to get the IPA.)

Within the recipes folder, I've made Theos Jailed projects with python scripts that automatically download the latest .deb files
and extract the tweaks. It then builds a tweaked IPA using the IPAs you fed it.
Just run `python3 [script] -h` for help.

It's highly recommended to use [this fork](https://github.com/kabiroberai/theos-jailed/pull/71)
of theos-jailed, for Substitute (A12) support.

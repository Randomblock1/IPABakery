#!/usr/bin/python3
# Randomblock1's AutoTweaker script.
# Downloads latest debs and uses them to tweak IPAs.
from random import choice
import libbakery
from getopt import getopt, GetoptError
from subprocess import run
from sys import argv
from pick import pick
import os
import shutil

ipa_path = None
opts = None

try:
    opts, args = getopt(argv[1:], "hlwi:")
except GetoptError:
    print("For help: ipabake.py -h")
    exit(2)

for opt, arg in opts:
    if opt == "-h":
        print(
            "\nUsage: ipabake.py [options]\n"
            "  -h           this help\n"
            "  -i [path]    specify path to ipa\n"
        )
        exit()
    elif opt == "-i":
        ipa_path = arg

options = ["YouTube", "Spotify", "Custom"]
result = pick(options, "Choose an app to tweak")
print("Getting latest dylibs...")
if result[0] == "YouTube":
    os.chdir("recipes/youtube")
    packages = libbakery.fetchpackages("https://apt.alfhaily.me/")
    libbakery.fetchdylib(
        "https://apt.alfhaily.me/",
        "me.alfhaily.cercube",
        "Cercube.dylib",
        packages,
        True,
    )
    if not os.path.isdir("Resources"):
        os.mkdir("Resources")
    if os.path.isdir("Resources/Cercube.bundle"):
        print("Deleting previous Cercube bundle for upgrade")
        shutil.rmtree("Resources/Cercube.bundle")
    os.rename(
        "tmp/Library/Application Support/Cercube/Cercube.bundle",
        "Resources/Cercube.bundle",
    )
    shutil.rmtree("tmp")
    print("Saved Cercube.bundle successfully.")
    workdir = "youtube"
elif result[0] == "Spotify":
    os.chdir("recipes/spotify")
    print("Getting latest dylibs...")
    packages = libbakery.fetchpackages("https://repo.dynastic.co/")
    libbakery.fetchdylib(
        "https://repo.dynastic.co/", "com.spos", "Sposify.dylib", packages
    )
    packages = libbakery.fetchpackages("https://julio.hackyouriphone.org/Packages")
    libbakery.fetchdylib(
        "https://julio.hackyouriphone.org/",
        "com.julioverne.spotilife",
        "Spotilife.dylib",
        packages,
    )
    workdir = "spotify"
elif result[0] == "Custom":
    print()
else:
    exit("Invalid choice: " + result[0])

print("All dylibs successfully fetched.")


print("\nBaking IPA.")
run(
    ["make", "clean", "all", "package", "FINALPACKAGE=1", "CODESIGN_IPA=0"],
    cwd="recipes/" + workdir,
)
print("\nDone. IPA is in packages folder.")

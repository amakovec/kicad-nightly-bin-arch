from get_latest_binary import get_latest_binary
from pkgbuild import pkgbuild_gen
from git import clone_from_aur, local_commit, push_to_aur, keyfile_from_heroku_configvar
from aur import get_aur_version
import sys

if __name__ == '__main__':
    launchpad_version, binary_url = get_latest_binary()
    aur_version = get_aur_version()

    if aur_version == launchpad_version:
        sys.exit()

    pkgbuild_gen(launchpad_version, binary_url, 'kicad-nightly.env')

    keyfile_from_heroku_configvar()
    repo = clone_from_aur()
    local_commit(launchpad_version, repo)
    push_to_aur(repo)

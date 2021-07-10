from get_latest_binary import get_latest_binary
from pkgbuild import pkgbuild_gen
from git import clone_from_aur, local_commit, push_to_aur, keyfile_from_heroku_configvar
from aur import get_aur_version
import sys

if __name__ == "__main__":
    # Get the URL and version of the latest successful build's binary on Launchpad
    launchpad_version, binary_url = get_latest_binary()

    # Get the version of the latest version on the AUR
    aur_version = get_aur_version()

    # If the latest version on Launchpad isn't newer than the version on the AUR, don't
    # udpate the AUR
    if aur_version == launchpad_version:
        sys.exit()

    # Generate a new PKGBUILD
    pkgbuild_gen(launchpad_version, binary_url, "kicad-nightly.env")

    # Write the SSH_KEYGEN envvar (configured in Heroku) to a file, so that it can be
    # used by dulwich
    keyfile_from_heroku_configvar()

    # Clone the latest repo from the AUR
    repo = clone_from_aur()

    # Commit the generated PKGBUILD to the cloned repo
    local_commit(launchpad_version, repo)

    # Push the repo with the new commit to the AUR
    push_to_aur(repo)

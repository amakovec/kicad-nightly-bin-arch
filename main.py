from get_latest_binary import get_latest_binary
from pkgbuild import pkgbuild_gen
from git import clone_from_aur, local_commit, push_to_aur, keyfile_from_heroku_configvar
from aur import get_aur_version
import sys
import argparse

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description='Generate a PKGBUILD for AUR package "kicad-nightly-bin"'
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Use when running the script on a local machine instead of Heroku.",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Use when dry-running the script."
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Use when forcing an update, even if a new binary is not yet available.",
    )
    args = parser.parse_args()

    # Get the URL and version of the latest successful build's binary on Launchpad
    launchpad_version, binary_url = get_latest_binary()

    # Get the version of the latest version on the AUR
    aur_version, aur_pkgrel = get_aur_version()

    # If the latest version on Launchpad isn't newer than the version on the AUR, don't
    # udpate the AUR
    if aur_version == launchpad_version and not args.force:
        sys.exit()
    elif aur_version == launchpad_version and args.force:
        new_version = launchpad_version
        new_pkgrel = str(int(aur_pkgrel) + 1)
    elif aur_version != launchpad_version:
        new_version = launchpad_version
        new_pkgrel = "1"

    # Generate a new PKGBUILD
    pkgbuild_gen(new_version, new_pkgrel, binary_url, "kicad-nightly.env")

    # Write the SSH_KEYGEN envvar (configured in Heroku) to a file, so that it can be
    # used by dulwich
    if not args.local:
        keyfile_from_heroku_configvar()

    # Clone the latest repo from the AUR
    repo = clone_from_aur()

    # Commit the generated PKGBUILD to the cloned repo
    local_commit(new_version + "-" + new_pkgrel, repo)

    # Push the repo with the new commit to the AUR
    if not args.dry_run:
        push_to_aur(repo)

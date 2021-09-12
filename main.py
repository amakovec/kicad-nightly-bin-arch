from get_latest_binary import get_latest_binary
from pkgbuild import pkgbuild_gen
from git import clone_from_aur, local_commit, push_to_aur, keyfile_from_heroku_configvar
from aur import get_aur_version
import sys
import argparse
import logging

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

    # Enable debug prints to console if testing locally
    if args.local:
        logging.basicConfig(level=logging.DEBUG)

    # Get the URL and version of the latest successful build's binary on Launchpad
    logging.info("Getting link to latest binary from Launchpad...")
    launchpad_version, binary_url = get_latest_binary()
    logging.info("Latest Launchpad version: " + launchpad_version)
    logging.info("Latest Launchpad binary URL: " + binary_url)

    # Get string of the latest version on the AUR
    logging.info("Getting string of the latest version on the AUR...")
    aur_version, aur_pkgrel = get_aur_version()
    logging.info("Latest AUR version: " + aur_version + "-" + aur_pkgrel)

    # If the latest version on Launchpad isn't newer than the version on the AUR, don't
    # udpate the AUR
    if aur_version == launchpad_version and not args.force:
        logging.info("No updates available on Launchpad.  Exiting...")
        sys.exit()
    elif aur_version == launchpad_version and args.force:
        logging.info(
            "No updates available on Launchpad, but update force was requested by user.  Updating..."
        )
        new_version = launchpad_version
        new_pkgrel = str(int(aur_pkgrel) + 1)
    elif aur_version != launchpad_version:
        logging.info("Update available on Launchpad.  Updating...")
        new_version = launchpad_version
        new_pkgrel = "1"
    logging.info("Will push new version: " + new_version + "-" + new_pkgrel)

    # Generate a new PKGBUILD
    logging.info("Generating new package build...")
    pkgbuild_gen(new_version, new_pkgrel, binary_url, "kicad-nightly.env")
    logging.info("PKGBUILD generation successful.")

    # Write the SSH_KEYGEN envvar (configured in Heroku) to a file, so that it can be
    # used by dulwich
    if not args.local:
        keyfile_from_heroku_configvar()

    # Clone the latest repo from the AUR
    logging.info("Cloning latest repo from AUR...")
    repo = clone_from_aur()
    logging.info("Cloning successful.")

    # Commit the generated PKGBUILD to the cloned repo
    logging.info("Commiting changes to local AUR repo.")
    local_commit(new_version + "-" + new_pkgrel, repo)
    logging.info("Local commit successful.")

    # Push the repo with the new commit to the AUR
    if not args.dry_run:
        logging.info("Pushing changes to AUR...")
        push_to_aur(repo)
        logging.info("Push to AUR successful.  Update successful!")
    else:
        logging.info(
            "Dry-run enabled, will not push to AUR. Update otherwise successful!"
        )

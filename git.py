from dulwich import porcelain
from shutil import copyfile, rmtree

import os

ssh_uri = "ssh://aur@aur.archlinux.org/kicad-nightly-bin.git"
keyfile = ".ssh/aur"
repo_name = "kicad-nightly-bin"
branch_name = "master"
author = "Andy Makovec <andymakovec@gmail.com>"


def keyfile_from_heroku_configvar():
    """
    Write the SSH_KEYGEN envvar (configured in Heroku) to a file, so that it can be used
    by dulwich
    """
    key = os.environ["AUR_SSHKEY"]
    with open(keyfile, "w") as f:
        f.write(key)


def clone_from_aur():
    """
    Clone the latest repo from the AUR

    :param repo: A git repository backed by local disk
    :type repo: dulwich.repo.Repo
    """
    try:
        rmtree(repo_name)
    except:
        pass
    repo = porcelain.clone(source=ssh_uri, target=repo_name, key_filename=keyfile)

    return repo


def local_commit(version, repo):
    """
    Commit the generated PKGBUILD to the cloned repo

    :param version: Version in format "datetime+abbreviatedcommithash"
    :type version: str
    :param repo: A git repository backed by local disk
    :type repo: dulwich.repo.Repo
    """
    for file in ["PKGBUILD", ".SRCINFO", "kicad-nightly.env"]:
        copyfile(file, repo_name + "/" + file)
        porcelain.add(repo, repo_name + "/" + file)

    porcelain.commit(repo=repo, message=version, committer=author, author=author)


def push_to_aur(repo):
    """Push the repo with the new commit to the AUR"""
    r = porcelain.push(
        repo=repo, remote_location=ssh_uri, refspecs=branch_name, key_filename=keyfile
    )

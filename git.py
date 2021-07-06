from dulwich import porcelain
from shutil import copyfile, rmtree

import os

ssh_uri = 'ssh://aur@aur.archlinux.org/kicad-nightly-bin.git'
keyfile = '.ssh/aur'
repo_name = 'kicad-nightly-bin'
branch_name = 'master'
author='Andy Makovec <andymakovec@gmail.com>'

def keyfile_from_heroku_configvar():
    key = os.environ['AUR_SSHKEY']
    with open(keyfile,"w") as f:
        f.write(key)

def clone_from_aur():
    try:
        rmtree(repo_name)
    except:
        pass
    repo = porcelain.clone(source=ssh_uri, target=repo_name, key_filename=keyfile)

    return repo

def local_commit(version, repo):
    # TODO: `makepkg --printsrcinfo > .SRCINFO`
    for file in ['PKGBUILD', '.SRCINFO', 'kicad-nightly.env']:
        copyfile(file, repo_name + '/' + file)
        porcelain.add(repo, repo_name + '/' + file)

    porcelain.commit(repo=repo, message=version, committer=author, author=author)

def push_to_aur(repo):
    r = porcelain.push(repo=repo, remote_location=ssh_uri, refspecs=branch_name, key_filename=keyfile)

if __name__ == '__main__':
    repo = clone_from_aur()
    local_commit('5.99', repo)
    push_to_aur(repo)

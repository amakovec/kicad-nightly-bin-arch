from get_latest_binary import get_latest_binary
from pkgbuild import pkgbuild_gen
from git import clone_from_aur, local_commit, push_to_aur, keyfile_from_heroku_configvar

if __name__ == '__main__':
    version, binary_url = get_latest_binary()
    pkgbuild_gen(version, binary_url, 'kicad-nightly.env')

    keyfile_from_heroku_configvar()
    repo = clone_from_aur()
    local_commit(version, repo)
    push_to_aur(repo)

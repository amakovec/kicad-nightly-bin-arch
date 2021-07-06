from launchpadlib.launchpad import Launchpad

def get_latest_binary():

    # Give a name to this python script (name doesn't matter, login to API not required)
    app_name='kicad-nightly-bin-arch'

    # https://launchpad.net/~kicad/+archive/ubuntu/kicad-dev-nightly
    launchpad = Launchpad.login_anonymously(app_name, 'production', version='devel')

    # ~kicad is a Public Team on Launchpad
    owner = launchpad.people['kicad']

    # The ~kicad team has 2 projects: kicad and kicad-dev-nightly
    archive = owner.getPPAByName(name='kicad-dev-nightly')

    # Generic ubuntu information
    ubuntu = launchpad.distributions["ubuntu"]
    series = ubuntu.current_series
    arch_series = series.getDistroArchSeries(archtag='amd64')

    # see "getPublishedBinaries" under https://launchpad.net/+apidoc/devel.html#archive
    # status='Published' will only return the latest binary
    binaries=archive.getPublishedBinaries(exact_match=True, distro_arch_series=arch_series, binary_name='kicad-nightly', status='Published')
    for version in binaries:
        # see https://launchpad.net/+apidoc/devel.html#binary_package_publishing_history
        binary_package_version = version.binary_package_version
        binary_url = version.binaryFileUrls()[0]

        # Taken from https://code.launchpad.net/~kicad/+recipe/kicadnightly
        # versioning: "{time}+{git-commit:kicad}~{revno}"
        version = binary_package_version.split('~')[0]
        return version, binary_url

if __name__ == '__main__':
    version, binary_url = get_latest_binary()
    print(version)
    print(binary_url)
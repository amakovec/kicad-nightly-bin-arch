import requests


def get_aur_version():
    response = requests.get(
        "https://aur.archlinux.org/rpc/?v=5&type=info&arg[]=kicad-nightly-bin"
    )
    json_data = response.json()
    package_version = json_data["results"][0]["Version"]
    package_version = package_version.split("-")[0]
    return package_version

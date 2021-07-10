import requests
import hashlib
from jinja2 import Template


def remote_sha256sum(url):
    """
    Get the sha256sum of a remote file located at a URL.

    :param url: The URL where the binary is located
    :type url: str
    :return: Hex-formatted sha256sum
    :rtype: str
    """
    binary = requests.get(url, stream=True)
    binary.raw.decode_content = True
    sha256sum = hashlib.sha256(binary.content).hexdigest()
    return sha256sum


def local_sha256sum(path):
    """
    Get the sha256sum of a local file.

    :param path: Path of the local file (either relative or absolute)
    :type path: str
    :return: Hex-formatted sha256sum
    :rtype: str
    """
    with open(path, "rb") as f:
        bytes = f.read()  # read entire file as bytes
        env_sum = hashlib.sha256(bytes).hexdigest()
    return env_sum


def jinja_wrapper(template_filename, output_filename, **kwargs):
    """
    Render a template with provided variables and write to an output file.

    :param template_filename: Path (absolute or relative) to template file
    :type template_filename: str
    :param output_filename: Path (absolute or relative) to output file
    :type output_filename: str
    """
    with open(template_filename) as file_:
        template = Template(file_.read())

    outputText = template.render(**kwargs)

    with open(output_filename, "w") as f:
        f.write(outputText)


def pkgbuild_gen(version, binary_url, env_path):
    """
    Generate PKGBUILD and .SRCINFO with latest build info

    :param version: Version in format "datetime+abbreviatedcommithash"
    :type version: str
    :param binary_url: URL of Launchpad build arm64 .deb
    :type binary_url: str
    :param env_path: Path (abolute or relative) of kicad-nightly.env
    :type env_path: str
    """
    binary_sum = remote_sha256sum(binary_url)
    env_sum = local_sha256sum(env_path)

    jinja_wrapper(
        template_file="PKGBUILD.template",
        output_file="PKGBUILD",
        version=version,
        binary_url=binary_url,
        binary_sha256sum=binary_sum,
        env_sha256sum=env_sum,
    )

    jinja_wrapper(
        template_file=".SRCINFO.template",
        output_file=".SRCINFO",
        version=version,
        binary_url=binary_url,
        binary_sha256sum=binary_sum,
        env_sha256sum=env_sum,
    )

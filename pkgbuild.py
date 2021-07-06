import requests
import hashlib
from jinja2 import Template

def binary_sha256sum(binary_url):
    binary = requests.get(binary_url, stream=True)
    binary.raw.decode_content = True
    sha256sum = hashlib.sha256(binary.content).hexdigest();
    return sha256sum

def env_sha256sum(env_path):
    with open(env_path,"rb") as f:
        bytes = f.read() # read entire file as bytes
        env_sum = hashlib.sha256(bytes).hexdigest()
    return env_sum

def jinja_wrapper(template_file, output_file, **kwargs):
    with open(template_file) as file_:
        template = Template(file_.read())

    outputText = template.render(**kwargs)

    with open(output_file,"w") as f:
        f.write(outputText)

def pkgbuild_gen(version, binary_url, env_path):
    binary_sum  = binary_sha256sum(binary_url)
    #binary_sum = 'abc123'
    env_sum = env_sha256sum(env_path)

    jinja_wrapper(template_file='PKGBUILD.template',
                  output_file='PKGBUILD',
                  version=version,
                  binary_url=binary_url,
                  binary_sha256sum=binary_sum,
                  env_sha256sum=env_sum)

    jinja_wrapper(template_file='.SRCINFO.template',
                  output_file='.SRCINFO',
                  version=version,
                  binary_url=binary_url,
                  binary_sha256sum=binary_sum,
                  env_sha256sum=env_sum)

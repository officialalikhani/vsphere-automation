from setuptools import setup,find_packages

def read_version():
    version = {}
    with open('vsphere_automation/version.py', 'r') as f:
        exec(f.read(), version)
        return version['__version__']


setup(
    name="vsphere-automation",
    version=read_version(),
    description="",
    url='https://github.com/officialalikhani/vsphere-automation',
    author="officialalikhani",
    license="",
    packages=find_packages(include=['vsphere_automation', 'vsphere_automation.*']),
    install_requires=open('requirements.txt').readlines(),
)

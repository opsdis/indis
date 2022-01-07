
from os.path import dirname, join

from setuptools import setup, find_packages


def read(fname):
    return open(join(dirname(__file__), fname)).read()


setup(
    name='indis',
    version_config={
        "template": "{tag}",
        "dev_template": "{tag}.dev{ccount}",
        "dirty_template": "{tag}.post{ccount}+git.{sha}.dirty",
        "starting_version": "0.0.1",
        "version_callback": None,
        "version_file": None,
        "count_commits_from_version_file": False,
        "branch_formatter": None
    },
    setup_requires=['setuptools-git-versioning'],
    packages=find_packages(exclude=['demo']),
    author='thenodon',
    author_email='ahaal@redbridge.se',
    url='https://github.com/opsdis/indis',
    license='GPLv3',
    include_package_data=True,
    zip_safe=False,
    description='indis - Icinga native director import service',
    install_requires=read('requirements.txt').split(),
    python_requires='>=3.8',
)

import re
from codecs import open
from os import path

from setuptools import setup

package_name = "GyaoDL"

root_dir = path.abspath(path.dirname(__file__))




with open(path.join(root_dir, package_name, '__init__.py')) as f:
    init_text = f.read()
    version = re.search(r'__version__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    license = re.search(r'__license__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author = re.search(r'__author__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    author_email = re.search(r'__author_email__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)
    url = re.search(r'__url__\s*=\s*[\'\"](.+?)[\'\"]', init_text).group(1)

assert version
assert license
assert author
assert author_email
assert url

if path.exists("README.md"):
    with open('README.md', encoding='utf-8') as f:
        long_description = f.read()
else:
    long_description = "..."

setup(
    name=package_name,
    packages=[package_name],

    version=version,

    license=license,

    install_requires=[],
    tests_require=[],

    author=author,
    author_email=author_email,
    long_description_content_type="text/markdown",

    url=url,

    description='This is a script to download videos from GYAO!',
    long_description=long_description,
    keywords='GYAO!, yahoo, Download, Movie, OnDemand',

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Video :: Capture',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)

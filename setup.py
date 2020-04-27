# BOTD - IRC channel daemon.
#
# setup.py

import importlib

from setuptools import setup

importlib.invalidate_caches()

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='2',
    url='https://bitbucket.org/botd/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTD is a IRC channel daemon serving 24/7 in the background.. no copyright. no LICENSE.",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib", "feedparser"],
    packages=["botd"],
    data_files = [('/etc/systemd/system', ['botd.service'])],
    scripts=["bin/bot", "bin/botcfg", "bin/botctl", "bin/botd", "bin/bothup", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

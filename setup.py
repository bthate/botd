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
    version='15',
    url='https://bitbucket.org/botlib/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTD is a IRC channel daemon serving 24/7 in the background, it installs it's own botd.service file and can thus survive reboots. BOTD contains no copyright or LICENSE and is placed in the public domain.",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["libobj", "botlib", "feedparser"],
    packages=["botd"],
    scripts=["bin/bot", "bin/botcfg", "bin/botd", "bin/bothup", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

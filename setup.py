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
    version='16',
    url='https://bitbucket.org/botlib/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTD - channel daemon serving 24/7 in the background.",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=False,
    install_requires=["botlib", "feedparser"],
    packages=["botd"],
    namespace_packages=["botd"],
    scripts=["bin/bcmd", "bin/bot", "bin/botd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

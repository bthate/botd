# BOTD - IRC channel daemon.
#
# setup.py

from setuptools import setup, find_namespace_packages

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='12',
    url='https://bitbucket.org/botd/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="BOTD is a IRC channel daemon serving 24/7 in the background.. no copyright. no LICENSE.",
    long_description=read(),
    long_description_content_type="text/x-rst",
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib"],
    packages=["botd"],
    scripts=["bin/bot", "bin/botd", "bin/botctl", "bin/botsrv", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

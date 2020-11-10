# BOTD - 24/7 channel daemon
#
#

from setuptools import setup

def mods():
    import os
    return [x[:-3] for x in os.listdir("mods") if x.endswith(".py")]

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='18',
    url='https://github.com/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="24/7 channel daemon",
    long_description=read(),
    license='Public Domain',
    install_requires=["botlib"],
    packages=["mods"],
    namespace_packages=["mods"],
    zip_safe=False,
    scripts=["bin/bot", "bin/botd"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

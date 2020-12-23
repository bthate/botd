from setuptools import setup

def read():
    return open("README.rst", "r").read()

setup(
    name='botd',
    version='23',
    url='https://github.com/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl', 
    description="24/7 channel daemon",
    long_description=read(),
    license='Public Domain',
    install_requires=["botlib"],
    packages=["botd"],
    namespace_packages=["botd"],
    zip_safe=False,
    scripts=["bin/bot", "bin/botcmd", "bin/botctl", "bin/botd", "bin/botinst", "bin/botudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

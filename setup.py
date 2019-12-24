from setuptools import setup

def readme():
    with open('README') as file:
        return file.read()

setup(
    name='botd',
    version='1',
    url='https://bitbucket.org/bthate/botd',
    author='Bart Thate',
    author_email='bthate@dds.nl',
    description="python3 channel bot daemon.",
    long_description=readme(),
    license='Public Domain',
    zip_safe=True,
    install_requires=["botlib", "feedparser"],
    packages=["botd"],
    scripts=["bin/bot", "bin/botd", "bin/toudp"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)

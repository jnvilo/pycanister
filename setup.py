import os

from setuptools import setup

PACKAGE="pycanister"
VERSION="0.0.1"
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name=PACKAGE,
    version=VERSION,
    packages=[PACKAGE],
    long_description = long_description,
    long_description_content_type="text/markdown",
    test_suite='tests',
    install_requires=["python-cloudflare",],
    author="Jason Viloria",
    author_email="jnvilo@gmail.com",
    url="https://github.com/jnvilo/cfctl",
    classifiers=[
        'Development Status :: 3 - Alpha',
        
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ],
)


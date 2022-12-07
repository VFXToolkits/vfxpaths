#!/usr/bin/env python
# -*- encoding: utf-8 -*-
import os
import re
from setuptools import setup, find_packages


with open(os.path.join(os.path.dirname(__file__), 'vfxpaths', 'version.py')) as f:
    _version = re.match(r'.*__version__ = \'(.*?)\'', f.read(), re.DOTALL).group(1)


setup(
    name='vfxpaths',
    version=_version,
    description='Common processing module of VFX path',
    long_description=open('README.rst').read(),
    keywords='vfx, vfxpath, vfxfile, paths, read, write',
    url='https://github.com/VFXToolkits/vfxpaths',
    author='zuokangbo',
    author_email='zuokangbo@outlook.com',
    license='MIT License',
    packages=[
        'vfxpaths',
    ],
    python_requires='>=3.7',
    zip_safe=False
)

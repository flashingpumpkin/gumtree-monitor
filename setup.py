#!/usr/bin/env python
from setuptools import setup, find_packages
import monitor

METADATA = dict(
    name='monitor',
    version=monitor.__version__,
    author='Alen Mujezinovic',
    author_email='flashingpumpkin@gmail.com',
    description='Cli tool to monitor gumtree feeds and send notifications',
    long_description='Cli tool to monitor gumtree feeds and send notifications',
    url='http://github.com/flashingpumpkin/monitor',
    keywords='gumtree feeds notification monitor',
    install_requires=['feedparser', 'requests', 'mail'],
    zip_safe=False,
    packages=find_packages(),
    entry_points = {
        'console_scripts' : [
            'gumtree-monitor=monitor:main'
        ]
    }
)

if __name__ == '__main__':
    setup(**METADATA)

#!/usr/bin/env python

from setuptools import setup

setup(
    name='hnscraper',
    version='0.1',
    description='Library to scrape content from the Hacker News website',
    author='Ed Parcell',
    author_email='ed.parcell@cobaltquantware.com',
    packages=['hnscraper'],
    install_requires=["mechanize >= 0.1.7",
                      "BeautifulSoup >= 3.0.7"
                      ])
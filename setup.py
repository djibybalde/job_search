# -*- coding: utf-8 -*-
"""
    Setup file for job_search.
    Use setup.cfg to configure your project.
"""

from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="job_search",
    version="0.0.1",
    description="Search and scrape job on fr.indeed.com!",
    py_modules=["indeed"],
    package_dir={"": "src"},

    long_description=long_description,
    long_description_content_type="text/markdown",

    url="https://github.com/djibybalde/myproject",
    author="Djiby BALDE",
    author_email="dybalde@gmail.com",

    package=find_packages(exclude=['tests', 'tests*']),  # docs
    test_suite='tests',
    tests_require=['six'],

    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine",
        ],
    },

    install_requires=[
        "blessings ~= 1.7",
     ],
)

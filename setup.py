#!/usr/bin/env python

from setuptools import setup, find_packages


def main():
    from abook2procmail import abook2procmail
    setup(
        # Metadata
        name="abook2procmail",
        version=abook2procmail.VERSION,
        description="A tool to generate procmail rules from abook.",
        author="Zoltan Puskas",
        author_email="zoltan@sinustrom.info",
        url="https://sinustrom.info/2020/08/09/address-book-based-e-mail-approval-in-procmail/",  # noqa: E501
        license=abook2procmail.LICENSE,
        project_urls={
            "Source Code": "https://github.com/zpuskas/abook2procmail",
            "Bug Traacker": "https://github.com/zpuskas/abook2procmail/issues",
        },
        long_description="A script to generate procmail allowlist rule include "
                         "rc files from abook address books.",
        python_requires='>=3.7.0',

        # Package data
        packages=find_packages(),
        entry_points={
            "console_scripts": [
                "abook2procmail=abook2procmail.abook2procmail:main",
            ],
        },

        install_requires=[
            "click>=7.1"
        ],

        classifiers=[
            'Environment :: Console',
            'License :: OSI Approved :: GNU Affero General Public License v3',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
        ],
    )


if __name__ == '__main__':
    main()

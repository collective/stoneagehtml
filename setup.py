from setuptools import find_packages
from setuptools import setup

import os


version = "1.0.0"


long_description = "\n\n".join([open("README.rst").read(), open("CHANGES.rst").read(),])


setup(
    name="StoneageHTML",
    version=version,
    description="Stone-Age HTML Filter: prepare documents for e-mail distribution",
    long_description=long_description,
    # Get more strings from http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    keywords="mail css",
    author="Malthe Borch",
    author_email="mborch@gmail com",
    maintainer="Johannes Raggam",
    maintainer_email="raggam-nl@adm.at",
    url="http://github.com/collective/stoneagehtml",
    license="LGPL - http://www.gnu.org/copyleft/lesser.html",
    packages=find_packages(exclude=["ez_setup"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=["setuptools", "BeautifulSoup4", "cssutils"],
    extras_require={
        "test": ["lxml",]
    }
)

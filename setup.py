from setuptools import setup, find_packages
import os

version = '0.2'

setup(name='StoneageHTML',
      version=version,
      description="Stone-Age HTML Filter: prepare documents for e-mail distribution",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        ],
      keywords='mail css',
      author='Malthe Borch',
      author_email='mborch@gmail com',
      maintainer="Johannes Raggam",
      maintainer_email="raggam-nl@adm.at",
      url='http://github.com/thet/stoneagehtml',
      license='LGPL - http://www.gnu.org/copyleft/lesser.html',
      packages=find_packages(exclude=['ez_setup']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'BeautifulSoup',
          'cssutils'
      ],
      )

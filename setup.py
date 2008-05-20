"""Stone-Age HTML Filter: prepare documents for e-mail distribution."""

classifiers = """\
Development Status :: 4 - Beta
Environment :: Web Environment
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Operating System :: OS Independent
Programming Language :: Python
Topic :: Internet
Topic :: Software Development :: Libraries :: Python Modules
Topic :: Text Processing :: Markup :: HTML
"""

from setuptools import setup, find_packages
import sys, os

doclines = __doc__.split("\n")

setup(name="StoneageHTML",
      version="0.1.5",
      maintainer="Malthe Borch",
      maintainer_email="mborch@gmail.com",
      license = "http://www.gnu.org/copyleft/lesser.html",
      platforms = ["any"],
      description = doclines[0],
      classifiers = filter(None, classifiers.split("\n")),
      long_description = "\n".join(doclines[2:]),
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      url='https://dev.serverzen.com/svn/public/projects/stoneagehtml',
      install_requires=['BeautifulSoup', 'cssutils'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

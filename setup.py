# -*- coding: utf-8 -*-
"""
This module contains the tool of jyu.rsslisting
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0.1'

setup(name='jyu.rsslisting',
      version=version,
      description="A page, which displays an RSS feeds (or aggregation of several feeds) in the same way as RSS portlet does",
      long_description=read('jyu/rsslisting/README.txt'),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='plone rss listing view',
      author='Asko Soukka',
      author_email='asko.soukka@iki.fi',
      maintainer='Jukka Ojaniemi',
      maintainer_email='jukka.ojaniemi@jyu.fi',
      url='http://svn.plone.org/svn/collective/jyu.rsslisting',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['jyu', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'feedparser',
                        # -*- Extra requirements: -*-
                        ],
      entry_points="""
      # -*- entry_points -*- 
      """,
      )

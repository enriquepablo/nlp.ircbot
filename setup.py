from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='nlp.ircbot',
      version=version,
      description="nl irc bot",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='nl irc bot',
      author='Enrique P\xc3\xa9rez Arnaud',
      author_email='enriquepablo@gmail.com',
      url='http://enriquepablo.github.com/nlp.ircbot',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['nlp'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )

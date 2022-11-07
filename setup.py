"""
Package setup for the egg
"""

from setuptools import setup, find_packages

with open('README.MD', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='sonarqube-api',
    version='0.0.1',
    platform='any',
    description='Package that creates simple APIs to interact with SonarQube',
    packages=find_packages(),
    url='https://github.com/peterdeames/sonarqube-api',
    keywords='sonar sonarqube',
    classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: DevOps Engineers',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          'Topic :: Utilities',
          ]
)
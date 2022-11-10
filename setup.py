"""
Package setup for the egg
"""

import setuptools

with open('README.MD', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name='sonarqube-client',
    version='0.0.1',
    description='Package that creates simple APIs to interact with SonarQube',
    packages=setuptools.find_packages(),
    url='https://github.com/peterdeames/sonarqube-api',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='sonar sonarqube',
    classifiers=[
          'Development Status :: 1 - Planning',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'Programming Language :: Python',
          'Topic :: Utilities',
          'Operating System :: OS Independent'
          ]
)

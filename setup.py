#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(name='bash-powerprompt',
      version='0.1.0',
      description='Powerful bash prompt based on Vim Powerline',
      long_description=open('README.md', 'r').read(),
      author='Arjan de Pooter',
      author_email='mail@arjandepooter.nl',
      url='https://github.com/MrHaas/bash-powerprompt',
      packages=['powerprompt'],
      scripts=['powerprompt/bin/bashpowerprompt.py'],
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Topic :: System :: Shells',
      ])
#!/usr/bin/env python

from setuptools import setup
import platform

packages = [
    'nitt_sw_login'
]

install_req = ["requests", "PyOpenSSL", "pyasn1", "urllib3"]

if platform.system() in ['Linux', 'Darwin']:
	install_req.append("ndg-httpsclient")

long_description = \
'''
A command line utility that logs you in the NITT Dell SonicWall, and
maintains a stable internet connection, without any time limit. (Only
for NIT-Trichy students)
'''

setup(name='nitt_sw_login',
      version='1.0',
      author='Shubham Dighe',
      author_email='digsblogger@gmail.com',
      license='BSD 3-clause "New" or "Revised" License',
      description='NITT Sonicwall Login Manager',
      long_description=long_description,
      url='https://github.com/digaru19/NITT-SonicWall-Login',
      keywords='nitt_sw_login nitt nit-trichy nitt-sw-login',
      classifiers=[
            'Environment :: Console',
            'Development Status :: 5 - Production/Stable',
            'Natural Language :: English',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP :: Session'
      ],
      packages=packages,
      install_requires=install_req,
      entry_points={
      		'console_scripts' : [
      				'nitt-sw-login=nitt_sw_login.__main__:main'
      			]
      	}
      )

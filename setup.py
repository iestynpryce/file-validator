try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'File validator',
    'author': 'Iestyn Pryce',
    'url': '',
    'download_url': '',
    'author_email': 'iestyn.pryce@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['validator'],
    'scripts': ['bin/validate_file.py'],
    'name': 'validator'
}

setup(**config)

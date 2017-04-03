from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name = 'django-cra-helper',
    version = '1.0.0',
    description = 'The missing piece of the Django + React puzzle',
    long_description = 'A Django app that allows you to easily incorporate create-react-app code in your Django project',
    url = 'https://github.com/MasterKale/django-cra-helper',
    author = 'Matthew Miller',
    author_email = 'kale@iammiller.com',
    license = 'MIT',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords = 'django react create-react-app integrate',
    packages = find_packages(exclude=['contrib', 'docs', 'tests']),
    download_url = 'https://github.com/MasterKale/django-cra-helper/archive/1.0.tar.gz',
    install_requires = [
        'bleach>=2'
    ],
)

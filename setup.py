from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='django-cra-helper',
    version='2.0.0',
    description='The missing piece of the Django + React puzzle',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/MasterKale/django-cra-helper',
    author='Matthew Miller',
    author_email='matthew@millerti.me',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='django react create-react-app integrate',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'django-proxy>=1.2.1',
    ],
)

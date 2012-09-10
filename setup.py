import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-polls',
    version='0.0.1',
    description='A simple polls app for django',
    long_description=read('README.md'),
    license=read('LICENSE'),
    author='noxan',
    author_email='contact@byteweaver.net',
    url='https://github.com/byteweaver/django-polls',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
    ],
)

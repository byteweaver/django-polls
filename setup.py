import os
from setuptools import setup, find_packages

import polls


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='django-polls',
    version=polls.__version__,
    description='A simple polls app for django',
    long_description=read('README.md'),
    license='MIT License',
    author='noxan',
    author_email='contact@byteweaver.net',
    url='https://github.com/byteweaver/django-polls',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Django',
        'django-extensions==1.3.11',
        'django-tastypie==0.12.1',
    ],
)

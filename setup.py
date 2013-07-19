# -*- mode: python; coding: utf-8; -*-
from setuptools import setup, find_packages

setup(
    name='imagestore',
    version='2.7.8',
    packages=find_packages(),
    install_requires=[
        'django',
        'sorl-thumbnail',
        'south',
        'django-fancy-autocomplete',
        'django-tagging',
    ],
    author='Pavel Zhukov',
    author_email='gelios@gmail.com',
    description='Gallery solution for django projects',
    long_description=open('README.rst').read(),
    license='GPL',
    keywords='django gallery',
    url='http://bitbucket.org/zeus/imagestore/',
    include_package_data=True
)

# (C) 2019 Airbus copyright all rights reserved
from setuptools import setup, find_packages

dependencies = ['QtPy','numpy']

setup(
    name='SurRender',
    version='6.0',
    author='berjaoui',
    author_email='surrender.software@airbus.com',
    packages=find_packages(),
    install_requires=dependencies,
    include_package_data=False,
    description='SurRender python interface',
    zip_safe=True
)


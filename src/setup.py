from setuptools import setup, find_packages

setup(
    name='regr',
    version='0.0.1',
    description='Core-package for regression tests.',
    long_description='Core-package for regression tests.',
    author='Hidetoshi Mochizuki',
    author_email='hidetoshi.mochizuki@ulsysems.co.jp',
    license='MIT',
    packages=find_packages(include=('drivers',)),
    test_suite='test',
)

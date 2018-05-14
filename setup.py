from setuptools import setup, find_packages
import glob

drivers = [x.replace('\\', '/') for x in glob.glob("src/drivers/*")]
print(drivers)

setup(
    name='regress',
    version='0.0.1',
    description='Core-package for regression tests.',
    long_description='Core-package for regression tests.',
    author='Hidetoshi Mochizuki',
    author_email='gmochmoch@gmail.com',
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    package_data={'drivers': drivers},
    include_package_data=True,
    install_requires=('selenium',),
    test_suite='src.test',
)

import sys

from setuptools import setup, find_packages


with open('README.rst') as _readme_file:
    readme = _readme_file.read()


tests_require = [
    'pytz',
]
if sys.version_info < (2, 7):
    tests_require += ['unittest2']

setup(
    name='validation',
    url='https://github.com/bwhmather/python-validation',
    version='0.4.0',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='Apache Software License',
    description=(
        "A library for runtime type checking and validation of python values"
    ),
    long_description=readme,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'six >= 1.10, < 2',
    ],
    tests_require=tests_require,
    packages=find_packages(),
    package_data={
        '': ['*.pyi'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
    test_suite='validation.tests.suite',
)

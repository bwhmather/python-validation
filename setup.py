from setuptools import setup, find_packages


setup(
    name='validation',
    url='https://github.com/JOIVY/validation',
    version='0.1.1',
    author='Ben Mather',
    author_email='bwhmather@bwhmather.com',
    maintainer='',
    license='BSD',
    description=(
        "A library for runtime type checking and validation of python values"
    ),
    long_description=__doc__,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'six >= 1.10, < 2',
    ],
    tests_require=[
        'pytz',
    ],
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

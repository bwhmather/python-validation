from setuptools import setup, find_packages


with open('README.rst') as _readme_file:
    readme = _readme_file.read()


tests_require = [
    'pytz', 'idna'
]

setup(
    name='validation',
    url='https://github.com/bwhmather/python-validation',
    version='0.8.0',
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
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=[
        'six >= 1.10, < 2',
    ],
    tests_require=tests_require,
    extras_require={
        'test': tests_require,
        'email': ['idna >= 2.0.0']
    },
    packages=find_packages(),
    package_data={
        '': ['*.pyi', 'py.typed'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
    test_suite='validation.tests.suite',
)

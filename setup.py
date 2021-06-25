from setuptools import setup, find_packages


def load_readme():
    with open('README.md', encoding='utf8') as readme:
        return readme.read()


REQUIRES = (
    'termcolor==1.1.0',

    # the dataclasses module is prebuilt into python>=3.7
    # For Python 3.6, it is supported using a backport
    'dataclasses; python_version < "3.7"',
)


EXTRAS = {
    'dev': (
        'pytest>=6.2, <6.3',
        'flake8>=3.9, <3.10'
    ),
    'yaml': (
        'pyyaml>=5.4, <5.5',
    ),
    'toml': (
        'toml>=0.10.2, <0.11',
    ),
}

EXTRAS['all'] = tuple(
    package
    for group in EXTRAS
    if group != 'dev'
    for package in EXTRAS[group]
)

EXTRAS['dev'] += EXTRAS['all']

setup(
    name='validit',
    description='Easily define and validate configuration file structures 📂🍒',
    version='1.3.1',
    author='RealA10N',
    author_email='downtown2u@gmail.com',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/RealA10N/validit',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=REQUIRES,
    extras_require=EXTRAS,
)

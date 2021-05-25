from setuptools import setup, find_packages


def load_readme():
    with open('README.md') as readme:
        return readme.read()


extras_require = {
    'dev': (
        'pytest>=6.2.4, <7',
    ),
    'yaml': (
        'pyyaml>=5.4.1, <6',
    ),
}

setup(
    name='configTemplate',
    version='0.0.1',
    author='RealA10N',
    author_email='downtown2u@gmail.com',
    description='Easily define and check configuration file structures',
    long_description=load_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/RealA10N/configTemplate',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Operating System :: OS Independent',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    extras_require=extras_require,
)

import re
from codecs import open

from setuptools import setup, find_packages

__version__ = '0.0.1'

# Get the long description from the README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# get the dependencies and installs
with open('requirements.txt', encoding='utf-8') as f:
    all_reqs = f.read().split('\n')

install_requires = [
    re.sub(r'--hash=.*', '', x.strip()) for x in all_reqs if 'git+' not in x
]
dependency_links = [
    x.strip().replace('git+', '') for x in all_reqs if x.startswith('git+')
]

setup_args = dict(
    name='pies',
    version=__version__,
    description='Pointless app',
    long_description=long_description,
    url='https://github.com/workiva/pies',
    download_url='https://github.com/workiva/pies/tarball/' + __version__,
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
    ],
    keywords='',
    packages=find_packages(exclude=['docs', 'tests*']),
    include_package_data=True,
    author='Eric Larssen',
    install_requires=install_requires,
    dependency_links=dependency_links,
    author_email='ericlarssen@workiva.com',
    entry_points={'console_scripts': ['pies=pies.scripts.pies:main']},
)

if __name__ == '__main__':
    setup(**setup_args)

import os, time

from setuptools import setup, find_packages


def read(filename):
    """Read file contents."""
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), filename))
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')

setup_args = dict(
    name='pies',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'pyformance'
        'app_intelligence'
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pies=pies:main'
        ]
    }
)

if __name__ == '__main__':
    setup(**setup_args)

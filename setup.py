import os
from setuptools import find_packages, setup


def get_version():
    import imp

    pkg_meta = imp.load_source('_pkg_meta', 'pies/web/_pkg_meta.py')

    return pkg_meta.version


def read(filename):
    """Read file content."""
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), filename))
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')


def get_requirements(filename):
    return [dep.strip() for dep in read(filename).split('\n') if dep.strip()]


def get_install_requires():
    return get_requirements('requirements.txt')


def get_test_requires():
    return get_requirements('requirements_dev.txt')


setup_args = dict(
    name='pies',
    version=get_version(),
    packages=find_packages(),
    namespace_packages=['pies', 'pies.scripts'],
    install_requires=get_install_requires(),
    tests_require=get_test_requires(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pies=pies.scripts.pies:main',
        ]
    },
)

if __name__ == '__main__':
    setup(**setup_args)

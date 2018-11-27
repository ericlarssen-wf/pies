import os

from setuptools import setup, find_packages


def read(filename):
    """Read file contents."""
    path = os.path.realpath(os.path.join(os.path.dirname(__file__), filename))
    with open(path, 'rb') as f:
        return f.read().decode('utf-8')


dependencies = [
    dep.strip() for dep in read('requirements.txt').split('\n') if dep.strip()]


def get_version():
    import imp

    pkg_meta = imp.load_source('_pkg_meta', 'k8s_migration/_pkg_meta.py')

    return pkg_meta.version


setup_args = dict(
    name='k8s_migration',
    version=get_version(),
    maintainer='Workiva InfRe <infre@workiva.com>',
    maintainer_email='infre@workiva.com',
    description='Utility for migrating services from Admiral to K8s',
    packages=find_packages(),
    install_requires=dependencies,
    entry_points={
        'console_scripts': [
            'k8s-migrate=k8s_migration.migrate.cli:main',
        ],
    },
)


if __name__ == '__main__':
    setup(**setup_args)

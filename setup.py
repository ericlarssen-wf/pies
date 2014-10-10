from setuptools import find_packages, setup
from pip.req import parse_requirements


def get_requirements(filename):
    reqs = parse_requirements(filename)
    return [str(r.req) for r in reqs]


def get_install_requires():
    return get_requirements('requirements.txt')


setup_args = dict(
    name='pies',
    version='0.0.1',
    packages=find_packages(),
    namespace_packages=['pies'],
    entry_points={
        'console_scripts': [
            'pies-test=pies.util:say_hello'
        ]
    }
)

if __name__ == '__main__':
    setup(**setup_args)

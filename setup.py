from setuptools import setup


setup(
    name='pilger-leap',
    version='0.0.1',
    packages=['pilgerleap'],
    package_dir={'': 'src'},
    long_description=open('README.md').read(),
    install_requires=[
        dep for dep in open('requirements.txt') if not dep.startswith('#')
    ],
)

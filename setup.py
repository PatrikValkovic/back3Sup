from setuptools import setup

setup(
    name='back3Sup',
    version='1.0.0',
    packages=['back3Su.py'],
    url='https://github.com/PatrikValkovic/back3Sup',
    license='MIT',
    author='Patrik Valkovic',
    author_email='patrik.valkovic@helsinki.fi',
    description='Exercise project to backup files to 3S service.',
    install_requires=[
        'boto3',
    ],
)

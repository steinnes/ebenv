from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession


setup(
    name='AWS Elasticbeanstalk environment extractor',
    version='0.1',
    description='',
    install_requires=[str(req.req) for req in parse_requirements("requirements.txt", session=PipSession())],
    entry_points='''
        [console_scripts]
        ebenv=ebenv:cli
    '''
)

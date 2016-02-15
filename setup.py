from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession


setup(
    name='ebenv',
    version='0.2',
    description='AWS Elastic Beanstalk environment dumper/extractor.',
    url='https://github.com/steinnes/ebenv',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['aws', 'elasticbeanstalk', 'environment'],
    install_requires=[str(req.req) for req in parse_requirements("requirements.txt", session=PipSession())],
    entry_points='''
        [console_scripts]
        ebenv=ebenv:cli
    '''
)

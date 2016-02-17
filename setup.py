import os
from setuptools import setup
from pip.req import parse_requirements
from pip.download import PipSession


def get_requirements():
    requirements = parse_requirements(
        os.path.join(os.path.dirname(__file__), "requirements.txt"),
        session=PipSession())
    return [str(req.req) for req in requirements]


setup(
    name='ebenv',
    version='0.2',
    description='AWS Elastic Beanstalk environment dumper/extractor.',
    url='https://github.com/steinnes/ebenv',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['aws', 'elasticbeanstalk', 'environment'],
    install_requires=get_requirements(),
    entry_points='''
        [console_scripts]
        ebenv=ebenv:cli
    '''
)

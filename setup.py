import codecs
import fastentrypoints
import os

from setuptools import setup


try:
    # pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # pip <= 9.0.3
    from pip.req import parse_requirements

try:
    # pip >= 10
    from pip._internal.download import PipSession
except ImportError:
    # pip <= 9.0.3
    from pip.download import PipSession


def get_requirements():
    requirements = parse_requirements(
        os.path.join(os.path.dirname(__file__), "requirements.txt"),
        session=PipSession())
    return [str(req.req) for req in requirements]


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='ebenv',
    version='0.3.0',
    description='AWS Elastic Beanstalk environment dumper/extractor.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/steinnes/ebenv',
    author='Steinn Eldjarn Sigurdarson',
    author_email='steinnes@gmail.com',
    keywords=['aws', 'elasticbeanstalk', 'environment'],
    install_requires=get_requirements(),
    packages=['ebenv'],
    entry_points='''
        [console_scripts]
        ebenv=ebenv:cli
    '''
)

import boto3
import click
import os
import sys


@click.group()
def cli():
    pass


def get_env(app_name, env_name, aws_region):
    client = boto3.client('elasticbeanstalk', region_name=aws_region)
    response = client.describe_configuration_settings(ApplicationName=app_name, EnvironmentName=env_name)
    try:
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Invalid status code returned: {}".format(response['ResponseMetadata']['HTTPStatusCode']))
    except KeyError as e:
        print "Unknown error ({}) in boto.client.describe_configuration_settings".format(e)
        raise

    env = {}
    settings = response['ConfigurationSettings'][0]
    for setting in settings['OptionSettings']:
        if setting['Namespace'] == 'aws:elasticbeanstalk:application:environment':
            env[setting['OptionName']] = setting['Value']

    return env


@cli.command('envdir')
@click.argument('app_name')
@click.argument('env_name')
@click.option('--target_dir', default='.env')
@click.option('--aws_region', envvar='AWS_REGION')
def envdir(app_name, env_name, target_dir, aws_region):
    env = get_env(app_name, env_name, aws_region)
    if not click.confirm("found {} vars, will write to '{}/*'".format(len(env), target_dir)):
        click.echo("Exiting..")
        sys.exit(1)

    if not os.path.exists(target_dir) and not os.path.isdir(target_dir):
        click.echo("{} did not exists, creating".format(target_dir))
        os.mkdir(target_dir)
    else:
        if os.path.exists(target_dir):
            click.echo("{} exists but isn't a directory, unable to continue".format(target_dir))
            sys.exit(2)

    for param in sorted(env.keys()):
        with open(os.path.join(target_dir, param), "w") as out:
            out.write("{}".format(env[param]))


@cli.command('env')
@click.argument('app_name')
@click.argument('env_name')
@click.option('--aws_region', envvar='AWS_REGION')
def env(app_name, env_name, aws_region):
    env = get_env(app_name, env_name, aws_region)

    for param in sorted(env.keys()):
        click.echo("{}={}".format(param, env[param]))


if __name__ == "__main__":
    cli()


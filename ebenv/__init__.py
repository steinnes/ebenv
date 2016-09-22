import boto3
import click
import os
import sys


ENV_VAR_NAMESPACE = 'aws:elasticbeanstalk:application:environment'


def get_client(region):
    return boto3.client('elasticbeanstalk', region_name=region)


@click.group()
def cli():
    pass


def get_env(app_name, env_name, aws_region):
    response = get_client(aws_region).describe_configuration_settings(ApplicationName=app_name, EnvironmentName=env_name)
    try:
        if response['ResponseMetadata']['HTTPStatusCode'] != 200:
            raise Exception("Invalid status code returned: {}".format(response['ResponseMetadata']['HTTPStatusCode']))
    except KeyError as e:
        print "Unknown error ({}) in boto.client.describe_configuration_settings".format(e)
        raise

    env = {}
    settings = response['ConfigurationSettings'][0]
    for setting in settings['OptionSettings']:
        if setting['Namespace'] == ENV_VAR_NAMESPACE:
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

    if not os.path.exists(target_dir):
        click.echo("{} did not exists, creating".format(target_dir))
        os.mkdir(target_dir)
    else:
        if os.path.exists(target_dir) and not os.path.isdir(target_dir):
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


@cli.command('copy')
@click.argument('app_name')
@click.argument('src_env_name')
@click.argument('dst_env_name')
@click.option('--remove', is_flag=True, default=False)
@click.option('--aws_region', envvar='AWS_REGION')
def copy(app_name, src_env_name, dst_env_name, remove, aws_region):
    src_env = get_env(app_name, src_env_name, aws_region)
    click.echo("Source environment '{}' has {} options".format(src_env_name, len(src_env)))
    removals = set()

    if remove:
        dst_env = get_env(app_name, dst_env_name, aws_region)
        for key in dst_env.keys():
            if key not in src_env:
                removals.add(key)
        click.echo("Will remove {} options from destination environment '{}'".format(len(removals), dst_env_name))

    options = [dict(
        Namespace=ENV_VAR_NAMESPACE,
        OptionName=key,
        Value=value) for key, value in src_env.iteritems()]

    remove_options = [dict(
        Namespace=ENV_VAR_NAMESPACE,
        OptionName=key) for key in removals]

    click.echo("Performing environment update...")
    client = get_client(aws_region)
    client.update_environment(
        ApplicationName=app_name,
        EnvironmentName=dst_env_name,
        OptionSettings=options,
        OptionsToRemove=remove_options)
    click.echo("Done, please check your EB web console to see the environment update progress")


if __name__ == "__main__":
    cli()


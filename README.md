# ebenv
AWS Elastic Beanstalk environment extractor/utility

This is a command line utility to manage environment variables from 
[AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/details/) app
environments, to either re-use the same configuration locally or to import
into another environment.

Currently two methods of extraction are supported, and one method to copy/sync
variables between environments:

## env

`env` dumps environment variables in a key=value format, example:

```
$ ebenv env app-name app-env-name
AWS_ACCESS_KEY_ID=abcdefghijklmnopqrstvwuxyz
BUGSNAG_API_KEY=deadbeefdeadbeefdeadbeef
PARAM1=value
PARAM2=value
...

$ ebenv env app-name app-env-name > envfile
$ docker run --rm -it --env-file=envfile app/name
...
```


## envdir

`envdir` dumps environment variables into an *envdir* as used by tools such as
djb's [envdir](https://cr.yp.to/daemontools/envdir.html), runit's
[chpst](http://smarden.org/runit/chpst.8.html), or one of the other clones,
example:

```
$ ebenv envdir app-name app-env-name
found 4 vars, will write to '.env/*' [y/N]: n
Exiting..
```

`envdir` will prompt before writing any files or creating the directory, and
a `--target_dir` option can be specified:

```
$ ebenv envdir app-name app-env-name --target_dir=.ebenv-copy
found 4 vars, will write to '.ebenv-copy/*' [y/N]: y
.ebenv-copy did not exists, creating

$ ls .ebenv-copy/
AWS_ACCESS_KEY_ID BUGSNAG_API_KEY   PARAM1            PARAM2

```

A simple `grep` can verify that the env files contain the desired data:
```
$ grep . .ebenv-copy/*
.ebenv-copy/AWS_ACCESS_KEY_ID:abcdefghijklmnopqrstvwuxyz
.ebenv-copy/BUGSNAG_API_KEY:deadbeefdeadbeefdeadbeef
.ebenv-copy/PARAM1:value
.ebenv-copy/PARAM2:value
```

## copy

`copy` copies the environment variables from one environment within an EB app
to another environment in the same app.  Can optionally be used to remove vars
from the destination environment, that are not found in the source environment.

```
$ ebenv copy app-name app-env-name new-app-env-name 
Source environment 'app-env-name'  has 22 options
Performing environment update...
Done, please check your EB web console to see the environment update progress
```

Right now `copy` will overwrite any values in the destination environment for
keys found in the source environment.  If you specify the `--remove` option,
it will remove any keys in the destination environment not found in the source
environment.

```
$ ebenv copy app-name app-env-name new-app-env-name
Source environment 'app-env-name'  has 22 options
Will remove 2 options from destination environment 'new-app-env-name'
...
```

This command is potentially very dangerous and destructive at this point,
especially if `--remove` is used.  Use with care.

# Setup

```
$ make
virtualenv venv
New python executable in /Users/ses/w/ebenv/venv/bin/python2.7
Also creating executable in /Users/ses/w/ebenv/venv/bin/python
Installing setuptools, pip, wheel...done.
venv/bin/python setup.py develop
...
```

Now `ebenv` is installed and available in the local `venv`, and can be used
either by activating the virtualenv (`source venv/bin/activate`) or by running
it directly from the venv: `venv/bin/ebenv`.


# Dependencies

`ebenv` depends on `boto3` and relies on boto3 being able to find standard AWS
credentials either via `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` env vars
in the local shell, or from `~/.aws/(config|credentials)`.


# Future

Write more options for `copy`, it might be useful to prompt for every 
detected change, to allow finer-grained copying of variables.  Maybe a
`--dryrun` switch to show the intended deltas.

Other useful commands might include a way to set an environment based
on an `env` file or an `envdir`, basically the opposite of those two
commands in the utility right now.

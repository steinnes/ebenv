# ebenv
AWS Elastic Beanstalk environment extractor

This is a command line utility to dump/extract environment variables from 
[AWS Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/details/) app
environments, to either re-use the same configuration locally or to import
into another environment.

Currently two methods of extraction are supported:

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

In the future I'll probably add a command to sync environment variables between
environments.  There are a few different ways of merging the vars (ie. how do
you treat variables only found in the target, and not the source) so for now I
am not venturing there.

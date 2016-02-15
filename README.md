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

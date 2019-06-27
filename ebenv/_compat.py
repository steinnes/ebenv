import sys

IS_PY2 = sys.version_info < (3,)


if IS_PY2:
    def iteritems(d):
        return d.iteritems()
else:
    def iteritems(d):
        return d.items()


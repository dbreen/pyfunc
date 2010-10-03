import getopt
import re
import sys

from titties.tittie import Tittie
from titties.constants import *


class InvalidArgumentException(Exception):
    pass

def usage():
    print """
Titties! Who doesn't love them? Unfortunately, this has nothing to do with
titties. This is a graph library that will plot functions on an x/y scale.

Usage: %(name)s [-d<dimensions>] [-x|y<x or y-axis scale>] arg1[, arg2, etc]

Options:

    -c, --colors:
        A comma-separated list of hex color values to use for each curve. The
        values will be rotated through; using just one value will use the same
        color for each curve. E.g., "-cffffff,ffdddd,336699" or "-cffffff".

    -d, --dimensions:
        Indicates the dimensions of the window that opens. Should be specified
        with the following format: <width>x<height>, e.g.: "400x400".

    -x, -y:
        Specifies the scale of the graph in given direction (x axis, or y
        axis). Uses the format <from>x<to>, for example to make a graph that
        extends from -5 to 5 on the x axis and 0 to 1.5 on y, use:
        "-x-5x5 -y0x1.5"

Functions:
    The python math library is available to use in functions. Most functions
    should be quoted on the command line to prevent bash from attempting to
    parse it. One special case is when the function starts with negative x -
    the command line argument parser assumes it as a switch and will fail. To
    work around this, use something like "0-x" or "(-x)".

Examples:

    $ python %(name)s x
    $ python %(name)s -y0x5 "abs(x)"
    $ python %(name)s --colors=336699,ffffee,990000,009900 --dimensions=800x600 -x-5x10 -y-5x10 x -x x**2 "5-x**2"
""" % {'name': sys.argv[0]}


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?c:d:x:y:",
                                       ["help", "colors=", "dimensions="])
    except getopt.GetoptError, e:
        print str(e)
        usage()
        sys.exit(1)

    defaults = {
        'dimensions': (400, 400),
        'x_scale': (-5.0, 5.0),
        'y_scale': (-5.0, 5.0),
        'colors': None
    }
    def scale(val, type_, key, defaults):
        x, _, y = val.partition('x')
        try:
            tup = (type_(x), type_(y))
        except Exception, e:
            raise InvalidArgumentEception, "'%s' not specified correctly (%s)" % (key, str(e))
        defaults[key] = tup

    try:
        for opt, arg in opts:
            if opt in ('-?', '--help'):
                usage()
                sys.exit(0)
            if opt in ('-d', '--dimensions'):
                scale(arg, int, 'dimensions', defaults)
            if opt in ('-x', '-y'):
                scale(arg, float, '%s_scale' % opt[1], defaults)
            if opt in ('-c', '--colors'):
                colors = arg.split(',')
                if not all([re.match(r'[0-9a-f]{6}', c) for c in colors]):
                    raise InvalidArgumentException, "Invalid color value specified"
                defaults['colors'] = ['#%s' % c for c in colors]
    except InvalidArgumentException, e:
        print "\n%s" % e
        usage()
        sys.exit(1)

    if len(args) == 0:
        print "You must specify at least one function. Use -? to display usage"
        sys.exit(1)

    funcs = []
    for f in args:
        try:
            # create a function from the arg and try it out with 0
            func = eval("lambda x: %s" % f)
            func(0)
        except Exception, e:
            print "Your function '%s' sucks. Here's the error:" % f
            print str(e)
            sys.exit(1)
        funcs.append(func)

    print "tittie args: ", defaults
    print "funcs: ", funcs

    tittie = Tittie(**defaults)
    for func in funcs:
        tittie.add_func(func)
    tittie.boob()

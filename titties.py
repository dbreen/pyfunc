import getopt
import sys

from titties.tittie import Tittie
from titties.constants import *


def usage():
    print """
Titties! Who doesn't love them? Unfortunately, this has nothing to do with
titties. This is a graph library that will plot functions on an x/y scale.

Usage: %s [-d<dimensions>] [-x|y<x or y-axis scale>] arg1[, arg2, etc]

Options:

    -d, --dimensions:
        Indicates the dimensions of the window that opens. Should be specified
        with the following format: <width>x<height>, e.g.: "400x400".

    -x, -y:
        Specifies the scale of the graph in given direction (x axis, or y
        axis). Uses the format <from>x<to>, for example to make a graph that
        extends from -5 to 5 on the x axis and 0 to 1.5 on y, use:
        "-x-5x5 -y0x1.5"
"""

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "?d:x:y:",
                                       ["help", "dimensions="])
    except getopt.GetoptError, e:
        print str(e)
        usage()
        sys.exit(1)

    defaults = {
        'dimensions': (400, 400),
        'x_scale': (-5.0, 5.0),
        'y_scale': (-5.0, 5.0)
    }
    def scale(val, type_, key, defaults):
        x, _, y = val.partition('x')
        try:
            tup = (type_(x), type_(y))
        except Exception, e:
            print "\n'%s' not specified correctly (%s)" % (key, str(e))
            usage()
            sys.exit(1)
        defaults[key] = tup

    for opt, arg in opts:
        if opt in ('-?', '--help'):
            usage()
            sys.exit(0)
        if opt in ('-d', '--dimensions'):
            scale(arg, int, 'dimensions', defaults)
        if opt in ('-x', '-y'):
            scale(arg, float, '%s_scale' % opt[1], defaults)

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
        tittie.plot(func)
    tittie.boob()

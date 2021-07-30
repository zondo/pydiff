"""Command line interface.
"""

import sys
import docopt

from . import __progname__, __version__
from .source import text_source
from .diff import diff_lines

USAGE = """
Usage: {prog} [options] FILE [FILE]

Description:
    Excel spreadsheet diff program.  With one arg, just shows a text
    representation of the spreadsheet.  With two args, shows a diff
    between the text representations of both of them.

Output options:
    -o FILE          Write to file instead of stdout

Other options:
    -t, --trace      Print traceback on error
    -h, --help       This help message
"""


def main(args=sys.argv[1:]):
    usage = USAGE.format(prog=__progname__)
    version = f"{__progname__} {__version__}"
    opts = docopt.docopt(usage, argv=args, version=version)

    try:
        run(opts)
    except Exception as exc:
        if opts["--trace"]:
            raise
        else:
            sys.exit("%s: error: %s" % (__progname__, str(exc)))


def run(opts):
    "Run the program."

    files = opts["FILE"]
    outfile = opts["-o"]

    if len(files) == 1:
        # One arg -- show text contents.
        path = files[0]
        output = text_source(path).lines()
    elif len(files) == 2:
        # Two args -- show diff.
        file1, file2 = files
        src1 = text_source(file1)
        src2 = text_source(file2)
        output = diff_lines(src1, src2)

    if outfile:
        f = open(outfile, "w")
    else:
        f = sys.stdout

    for line in output:
        f.write(line + "\n")


if __name__ == "__main__":
    main()

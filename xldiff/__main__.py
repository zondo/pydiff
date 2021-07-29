"""Main entry point.

TODO: improve arg parsing
"""

import sys

from .source import text_source
from .diff import diff_lines


def main():
    if len(sys.argv) == 2:
        # One arg -- show text contents.
        path = sys.argv[1]
        output = text_source(path).lines()
    elif len(sys.argv) > 2:
        # Two args -- show diff.
        file1, file2 = sys.argv[1:3]
        src1 = text_source(file1)
        src2 = text_source(file2)
        output = diff_lines(src1, src2, context=True)
    else:
        sys.exit(f"Usage: {sys.argv[0]} FILE1 [FILE2]")

    for line in output:
        print(line)


if __name__ == "__main__":
    main()

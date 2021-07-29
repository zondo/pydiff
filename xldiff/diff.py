"""Text diff functions.
"""

import difflib


def diff_lines(src1, src2, context=False, ignoreblank=True, contextlines=3):
    "Yield diff lines twixt two text sources."

    lines1 = src1.lines()
    lines2 = src2.lines()

    if ignoreblank:
        lines1 = (line for line in lines1 if line)
        lines2 = (line for line in lines2 if line)

    if context:
        func = difflib.context_diff
    else:
        func = difflib.unified_diff

    return func(list(lines1), list(lines2), str(src1), str(src2),
                lineterm="", n=contextlines)

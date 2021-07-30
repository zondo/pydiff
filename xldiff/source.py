"""Sources of text to diff.

TODO: consider removing xls support
"""

import xlrd
import openpyxl
import warnings


def text_source(path):
    "Return a TextSource for a path based on its suffix."

    for cls in sources:
        if path.endswith(cls.suffixes):
            src = cls(path)
            src.filename = path
            return src

    raise RuntimeError("no reader found for file '%s' (unknown suffix)" % path)


class TextSource(object):
    "Base class of sources of text lines."

    # Name of the source file.
    filename = None

    # Tuple of file suffixes used.  Must contain the period.
    suffixes = ()

    def __init__(self, path):
        raise NotImplementedError

    def lines(self):
        "Yield text lines."
        raise NotImplementedError

    def __repr__(self):
        return "<{}: {}>".format(self.__class__.__name__, self.filename)

    def __str__(self):
        return self.filename


class Spreadsheet(object):
    sheetformat = " Sheet: %s "
    separator = "\t"
    splitnewlines = False
    numformat = "%.12g"

    def sheetname(self, name, width=80, fillchar="-"):
        name = (self.sheetformat % name).center(width, fillchar)
        return "\n" + name + "\n"

    def cell_lines(self, cellrow, celltotext):
        values = map(celltotext, cellrow)
        values = filter(lambda x: x, values)
        line = self.separator.join(values).rstrip()

        if self.splitnewlines:
            for string in line.split("\n"):
                yield string
        else:
            yield line.replace("\n", " ")


class Excel(TextSource, Spreadsheet):
    suffixes = (".xls",)

    def __init__(self, path):
        self.book = xlrd.open_workbook(path)

    def lines(self):
        from xlrd import XL_CELL_NUMBER

        def totext(cell):
            if cell.ctype == XL_CELL_NUMBER:
                return self.numformat % cell.value
            else:
                return str(cell.value)

        for idx in range(self.book.nsheets):
            sheet = self.book.sheet_by_index(idx)
            yield self.sheetname(sheet.name)

            for row in range(sheet.nrows):
                cells = sheet.row_slice(row)
                yield from self.cell_lines(cells, totext)


class Excel2007(TextSource, Spreadsheet):
    suffixes = (".xlsx", ".xlsm")

    def __init__(self, path):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.book = openpyxl.load_workbook(path, data_only=True)

    def lines(self):
        def totext(cell):
            return str(cell.value or "")

        for name in self.book.sheetnames:
            sheet = self.book[name]
            yield self.sheetname(name)

            for cells in sheet.rows:
                yield from self.cell_lines(cells, totext)


# List of sources.
sources = [Excel, Excel2007]

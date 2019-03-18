# encoding=utf-8
import re


RE_BOOK = re.compile(r"""
    ((\d\s)?[А-Я][а-я]+)\.?\s*                  # book short title
    (,\s*\d+\s*зач\.\s*(\([^\)]+\))?)?,?\s*     # text before chapter
    ([IVXL]+)[^А-Яа-я\.\<\>\(\)]+[.;,]?         # chapter with lines
""", re.VERBOSE)

# using [^IVXL] due to possibility of unknown unicode range symbol
RE_CHAPTER = re.compile(r"""
    ((([IVXL]+),\s*([^IVXL]+)([IVXL]+),\s*(.+))     # type 1: chapter's range
    |
    ([IVXL]+),([^\<\>\(\)]+))                       # type 2: chapter lines
""", re.VERBOSE)

# using . instead of - due to possibility of unknown unicode range symbol
RE_CHAPTER_LINE_RANGE = re.compile(r"(\d+)\s*.\s*(\d+)")

RE_LINE_INT = re.compile(r"(\d+)")


def rim2arab(num):
    """Convert Latin numbers to Arabic:
    L - 50
    X - 10
    V - 5
    I - 1

    :type num: str
    :rtype: int
    """
    res = 0
    lt = False
    ltx = False
    for c in num:
        if c == "L":
            if ltx:
                res += 30
            else:
                res += 50
            lt = False
            ltx = False
        elif c == "X":
            if lt:
                res += 8
            else:
                res += 10
            lt = False
            ltx = True
        elif c == "V":
            if lt:
                res += 3
            else:
                res += 5
            lt = False
            ltx = False
        elif c == "I":
            res += 1
            lt = True
            ltx = False
    return res


class RefBook:
    """Each bible book must have book short title
    and one or set of chapters.
    Each chapter is presented by sequence of lines:
    VII, 1-3, 5-8, 9, 10
    Book instance chapters are list of dict like:
    {"chapter__num": int, "num__gte": int, "num__lte": int}
    which can be used directly in Django model's filters
    """

    def __init__(self, book, chapters=None):
        self.book = book
        self.chapters = chapters or []
        self.chapters_query = None

    def __str__(self):
        return "book={}, chapters={}".format(self.book, self.chapters)

    def __eq__(self, other):
        if isinstance(other, RefBook):
            res = self.book == other.book and len(self.chapters) == len(other.chapters)
            if res:
                for i, ch in enumerate(self.chapters):
                    res = res and ch == other.chapters[i]
                    if not res:
                        break
            return res
        return False

    def __parse_lines(self, chapter, lines, range_start=False, range_end=False):
        """Parsing sequence of lines numbers separated by ','.
        It can be single lines (int) or ranges (int - int).
        For chapter's range:
        If chapter's range start line sequence ends with single line
        all lines greater then this line should be taken.
        If chapter's range end line sequence starts with single line
        all lines less then this line should be taken.

        :range_start: should be num__gte
        :range_end: should be num__lte
        """
        _arr = lines.split(",")
        _arr_len = len(_arr)
        _num_postfix = ""
        if range_start:
            _num_postfix = "__gte"
        elif range_end:
            _num_postfix = "__lte"

        for i, lq in enumerate(_arr):
            _lines = lq.replace(".", "").strip()
            if not _lines:
                continue
            _m = RE_CHAPTER_LINE_RANGE.match(_lines)
            if _m:
                # line is a range:
                ls = _m.group(1)
                le = _m.group(2)
                self.chapters.append(
                    {"chapter__num": chapter, "num__gte": int(ls), "num__lte": int(le)}
                )
            else:
                # line is a single int:
                _m = RE_LINE_INT.search(_lines)
                if _m:
                    ln = int(_m.group(1))
                    _num = "num"
                    if _num_postfix:
                        if i == _arr_len - 1 and range_start or i == 0 and range_end:
                            _num += _num_postfix
                            _num_postfix = ""
                    self.chapters.append(
                        {"chapter__num": chapter, _num: ln}
                    )
                else:
                    print("[ERROR]: Can't parse chapter lines: {}".format(_lines))
                    continue

    def parse_chapters(self, line):
        """Chapters are presented by sequence of
        latin numbers with line sequences separated by ';'
        """
        self.chapters_query = line
        endpos = line.count(";")
        for raw in line.split(";"):
            chapter = raw.strip()
            if not chapter:
                continue

            m = RE_CHAPTER.search(chapter)
            if not m:
                continue

            endpos += m.end()
            _parsed = m.groups()
            if _parsed[-1]:
                # type 2:
                ch = rim2arab(_parsed[-2])
                self.__parse_lines(ch, _parsed[-1])
            else:
                # type 1:
                ch1, _lines1, ch2, _lines2 = _parsed[2:6]
                arab_ch1 = rim2arab(ch1)
                arab_ch2 = rim2arab(ch2)
                self.__parse_lines(arab_ch1, _lines1, range_start=True)
                for ch in range(arab_ch1+1, arab_ch2):
                    self.chapters.append({"chapter__num": ch})
                self.__parse_lines(arab_ch2, _lines2, range_end=True)
        return endpos


class MatchBook:

    def __init__(self, line, start=0, endpos=0, book=None):
        self.line = line
        self.start = start
        self.endpos = endpos
        self.book = book

    def __str__(self):
        return "span=({}:{}), {}".format(self.start, self.endpos, self.book)

    def __eq__(self, other):
        if isinstance(other, MatchBook):
            return (self.start == other.start and self.endpos == other.endpos and
                    self.book == other.book)
        return False

    @property
    def match(self):
        return self.line[self.start:self.endpos]


class RefParser:
    """Parse Bible reference patterns into a list of MatchBooks
    """

    def __init__(self, line=None):
        self.refs = []
        if line:
            self.parse(line)

    def parse(self, line):
        for m in RE_BOOK.finditer(line):
            _line = line[m.start():m.end()]
            # cutting prefix text:
            _start = _line.index(m.group(5))
            book = RefBook(m.group(1))
            endpos = m.start() + _start + book.parse_chapters(_line[_start:m.end()])
            if book.chapters:
                self.refs.append(
                    MatchBook(line, start=m.start(), endpos=endpos, book=book)
                )


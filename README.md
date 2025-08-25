# bible-ref-parser
Parsing of a string reference to Bible text lines (Russian)

String reference is presented as a Short Title of a Book with one or more chapters which are written in upper latin letters with a range or separate arabic numbers of Bible lines. All chapters are splitted by ';'. Lines splitted by ','.

##### Example

  line = "Солом. IV, 7, 16-17, 19-20;V, 1-7."

## Usage
Just pass a line to a parser:

```python
from ref_parser import RefParser

line = "Солом. IV, 7, 16-17, 19-20;V, 1-7."

parser = RefParser(line)

for m in parser.refs:
    print(m.match)
    print(m.book)
```

or you may use it to collect refs from a lot of lines:

```python
parser = RefParser()
    
for line in lines:
    parser.parse(line)
```

#### RefParser.refs
The list of MatchBook instances.
If parser finds a book in a line it creates a MatchBook instance with start and endpos positions.
Parser finds a book only when it recognises a short title and one or more chapters with strings.

#### MatchBook.match
Returns the substring with matched Bible reference.

#### MatchBook.book
The RefBook object. RefBook must be provided with short title and list of chapters.

#### RefBook.book
The short title of a Bible book (For example: In - Ioann)

#### RefBook.chapters
The list of chapters which are presented as dictionaries:

    {"chapter__num": int, "num__gte": int, "num__lte": int}

where `chapter__num` is a number of a chapter, `num__gte` and `num__lte` are the borders of a chaptere's lines range.

### Example

```python
line = "Солом. IV, 7, 16-17, 19-20;V, 1-7."
parser = RefParser(line)
book = parser.refs[0].book
print(book.book)
# Солом
print(book.chapters)
# [   {'chapter__num': 4, 'num': 7},
#     {'chapter__num': 4, 'num__gte': 16, 'num__lte': 17},
#     {'chapter__num': 4, 'num__gte': 19, 'num__lte': 20},
#     {'chapter__num': 5, 'num__gte': 1, 'num__lte': 7}]
```

Here you can read the above quote of Solomon book: [Солом. IV, 7, 16-17, 19-20;V, 1-7](https://st-gospel.ru/bible/lines/?b=Solom&r=IV%2C%207%2C%2016%E2%80%9317%2C%2019%E2%80%9320%3BV%2C%201%E2%80%937)

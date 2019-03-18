import pytest

from .ref_parser import RefParser, MatchBook, RefBook


PARAMS = [
    {
        "ref": "Мк., 57 зач.,XII, 38–44",
        "res": [
            RefBook(
                book="Мк",
                chapters=[
                    {"chapter__num": 12, "num__gte": 38, "num__lte": 44},
                ])
            ],
    },
    {
        "ref": " Предтечи: 1. Ис.XL, 1-3, 9; XLI, 17-18; XLV, 8; XLVIII, 20-21; LIV, 1;",
        "res": [
            RefBook(
                book="Ис",
                chapters=[
                    {"chapter__num": 40, "num__gte": 1, "num__lte": 3},
                    {"chapter__num": 40, "num": 9},
                    {"chapter__num": 41, "num__gte": 17, "num__lte": 18},
                    {"chapter__num": 45, "num": 8},
                    {"chapter__num": 48, "num__gte": 20, "num__lte": 21},
                    {"chapter__num": 54, "num": 1},
                ]
            ),
        ],
    },
    {
        "ref": "Ис., XL, 8 – XLII, 5.",
        "res": [
            RefBook(
                book="Ис",
                chapters=[
                    {"chapter__num": 40, "num__gte": 8},
                    {"chapter__num": 41},
                    {"chapter__num": 42, "num__lte": 5},
                ]
            ),
        ],
    },
    {
        "ref": "Лит. – Евр., 329 зач. (от полý),XI, 24–26, 32 – XII, 2.",
        "res": [
            RefBook(
                book="Евр",
                chapters=[
                    {"chapter__num": 11, "num__gte": 24, "num__lte": 26},
                    {"chapter__num": 11, "num__gte": 32},
                    {"chapter__num": 12, "num__lte": 2},
                ]
            ),
        ],
    },
    {
        "ref": "Лк.,XXIII, 39–43;",
        "res": [
            RefBook(
                book="Лк",
                chapters=[
                    {"chapter__num": 23, "num__gte": 39, "num__lte": 43},
                ]
            ),
        ],
    },
    {
        "ref": "Ев. составное: Мф., 110 зач.,XXVII, 1–44;Лк.,XXIII, 39–43;Мф.,XXVII, 45–54;Ин.,XIX, 31–37;Мф.,XXVII, 55–61.",
        "res": [
            RefBook(
                book="Мф",
                chapters=[
                    {"chapter__num":  27, "num__gte": 1, "num__lte": 44},
                ]
            ),
            RefBook(
                book="Лк",
                chapters=[
                    {"chapter__num": 23, "num__gte": 39, "num__lte": 43},
                ]
            ),
            RefBook(
                book="Мф",
                chapters=[
                    {"chapter__num":  27, "num__gte": 45, "num__lte": 54},
                ]
            ),
            RefBook(
                book="Ин",
                chapters=[
                    {"chapter__num":  19, "num__gte": 31, "num__lte": 37},
                ]
            ),
            RefBook(
                book="Мф",
                chapters=[
                    {"chapter__num":  27, "num__gte": 55, "num__lte": 61},
                ]
            ),
        ],
    },
    {
        "ref": " На 6-м часе: Зах.VIII, 7-17.  На веч.: Зах.VIII, 19-23.  Предтечи: 1. Ис.XL, 1-3, 9; XLI, 17-18; XLV, 8; XLVIII, 20-21; LIV, 1;  2. Мал.III, 1-3, 5-7, 12, 17-18; IV, 4-6;  3. Прем. Солом. IV, 7, 16-17, 19-20;V, 1-7. 1 Пет., 62 зач.,IV, 12 – V, 5. Мк., 57 зач.,XII, 38–44,и за пятницу (под зачало): 2 Пет., 64 зач.,I, 1–10.Лк., 51 зач. (от полý),X, 19–21",
        "res": [
            RefBook(
                book="Зах",
                chapters=[
                    {"chapter__num": 8, "num__gte": 7, "num__lte": 17},
                ]
            ),
            RefBook(
                book="Зах",
                chapters=[
                    {"chapter__num": 8, "num__gte": 19, "num__lte": 23},
                ]
            ),
            RefBook(
                book="Ис",
                chapters=[
                    {"chapter__num": 40, "num__gte": 1, "num__lte": 3},
                    {"chapter__num": 40, "num": 9},
                    {"chapter__num": 41, "num__gte": 17, "num__lte": 18},
                    {"chapter__num": 45, "num": 8},
                    {"chapter__num": 48, "num__gte": 20, "num__lte": 21},
                    {"chapter__num": 54, "num": 1},
                ]
            ),
            RefBook(
                book="Мал",
                chapters=[
                    {"chapter__num": 3, "num__gte": 1, "num__lte": 3},
                    {"chapter__num": 3, "num__gte": 5, "num__lte": 7},
                    {"chapter__num": 3, "num": 12},
                    {"chapter__num": 3, "num__gte": 17, "num__lte": 18},
                    {"chapter__num": 4, "num__gte": 4, "num__lte": 6},
                ]
            ),
            RefBook(
                book="Солом",
                chapters=[
                    {"chapter__num": 4, "num": 7},
                    {"chapter__num": 4, "num__gte": 16, "num__lte": 17},
                    {"chapter__num": 4, "num__gte": 19, "num__lte": 20},
                    {"chapter__num": 5, "num__gte": 1, "num__lte": 7},
                ]
            ),
            RefBook(
                book="1 Пет",
                chapters=[
                    {"chapter__num": 4, "num__gte": 12},
                    {"chapter__num": 5, "num__lte": 5},
                ]
            ),
            RefBook(
                book="Мк",
                chapters=[
                    {"chapter__num": 12, "num__gte": 38, "num__lte": 44},
                ]
            ),
            RefBook(
                book="2 Пет",
                chapters=[
                    {"chapter__num": 1, "num__gte": 1, "num__lte": 10},
                ]
            ),
            RefBook(
                book="Лк",
                chapters=[
                    {"chapter__num": 10, "num__gte": 19, "num__lte": 21},
                ]
            ),
        ],
    },
]


@pytest.fixture(params=PARAMS)
def testcase(request):
    return request.param


def test_parser(testcase):
    line = testcase["ref"]
    rp = RefParser(line)
    for i, m in enumerate(rp.refs):
        assert m.book == testcase["res"][i]


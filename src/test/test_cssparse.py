"""
test_cssparse.py

TODO insert description

"""

from cssparse import to_ast


def test_to_ast():
    css1 = ("margin-bottom:3em;  "
            "margin-top:2em; "
            "border: solid black 1px")

    css2 = ("border:solid black 1px;"
            "margin-bottom:  3em; "
            "margin-top:2em")

    res1 = to_ast(css1)
    res2 = to_ast(css2)

    assert res1 == res2
"""
cssparse.py

Parses CSS strings.

"""

import cssutils


def to_ast(css):
    """
    Our "AST" is a set of (property, value, priority) tuples, one per CSS
    statement. Value strings are normalized by cssutils.
    """
    parsed = cssutils.parseStyle(css)
    return frozenset(simplify(x) for x in parsed.children())


def to_str(ast):
    """
    Converts the "AST" / set representation of a block of CSS to a string.
    """
    output = ['\n']

    for property, value, priority in ast:
        assert not priority  # TODO handle case
        line = '    %s: %s;\n' % (property, value)
        output.append(line)

    return ''.join(output)


def simplify(p):
    """
    Returns just the bits we care about.
    """
    return p.name, p.value, p.priority
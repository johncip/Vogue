"""
vogue.py

Externalizes style tags and inline stylesheets.

"""

from HTMLParser import HTMLParser

from cssparse import to_ast, to_str


def partition(items, pred):
    """
    Returns a list of items which satisfy the predicate, and a list of items which don't.
    """
    yes = [x for x in items if pred(x)]
    no = [x for x in items if not pred(x)]
    return yes, no


class Parser(HTMLParser):
    """
    """

    def __init__(self, prefix):
        self.out = []
        self.sty = {}
        self.next = 1
        self.prefix = prefix

        HTMLParser.__init__(self)

    def feed(self, data):
        """
        Empty storage for a new output file is created for each new input file.
        """
        self.out = []
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        """
        Appends start tags to the output.
        If a style tag is present, its contents are added to the current
        stylesheet, and it is replaced by a class tag pointing to the same
        style information.
        """
        pred = lambda x: x[0] == 'style'

        styles, butes = partition(attrs, pred)
        butes = ['%s="%s"' % x for x in butes]
        styles = [x[1] for x in styles]

        if styles:
            s = to_ast(styles[0])
            if s not in self.sty:
                self.sty[s] = self.next
                self.next += 1
            butes.append('class="%s%s"' % (self.prefix, self.sty[s]))

        res = '<' + tag
        if butes:
            res += ' '
        res += " ".join(butes) + '>'

        self.out.append(res)

    def handle_startendtag(self, tag, attrs):
        """
        Start/end tags are treated the same as start tags.
        """
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        """
        Appends the end tags to the output.
        """
        res = '</' + tag + '>'
        self.out.append(res)

    def handle_data(self, data):
        """
        Appends the data to the output.
        """
        self.out.append(data)

    def stylesheet(self):
        """
        Returns the current stylesheet as a string.
        """
        fmt = ".%s%s { %s }\n"
        classes = sorted([(v, k) for (k, v) in self.sty.items()])
        out = (fmt % (self.prefix, cls, to_str(cset)) for cls, cset in classes)
        return '\n'.join(out)
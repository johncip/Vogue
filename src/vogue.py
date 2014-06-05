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

    # TODO feed_many

    def feed(self, data):
        """
        Empty storage for a new output file is created for each new input file.
        """
        self.out = []
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attributes):
        """
        Appends start tags to the output.
        If a style tag is present, its contents are added to the current
        stylesheet, and it is replaced by a class tag pointing to the same
        style information.
        """
        pred = lambda x: x[0] == 'style'
        styles, attrs = partition(attributes, pred)
        attrs = ['%s="%s"' % (a, v) for (a, v) in attrs]

        if styles:
            _, value = styles[0]  # list has one 2-tuple
            s = to_ast(value)

            # create a new entry
            if s not in self.sty:
                self.sty[s] = self.next
                self.next += 1
            attribute = 'class="{prefix}{num}"'.format(prefix=self.prefix,
                                                       num=self.sty[s])
            attrs.append(attribute)


        res = '<{tag}{attrs_str}>'.format(tag=tag, attrs_str=(' ' + ' '.join(
            attrs) if attrs else ' '))

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
        classes = sorted([(v, k) for (k, v) in self.sty.items()])
        fmt = ".%s%s { %s }\n"
        out = (fmt % (self.prefix, cls, to_str(cset)) for cls, cset in classes)

        return '\n'.join(out)
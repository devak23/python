import re


# re.findall returns a list with all non overlapping matches of the regular expression, as a list of strings
RE_WORD = re.compile(r'\w+')


class Sentence:
    def __init__(self, text):
        self.text = text
        self.words = RE_WORD.findall(self.text)

    def __repr__(self):
        return 'Sentence({})'.format(self.text)

    def __getitem__(self, i):
        """
        Whenever the interpreter needs to iterate over an object x, it automatically calls iter(x).
        The iter built-in function:
        1. Checks whether the object implements __iter__, and calls that to obtain an iterator.
        2. If __iter__ is not implemented, but __getitem__ is implemented, Python creates
        an iterator that attempts to fetch items in order, starting from index 0 (zero).
        3. If that fails, Python raises TypeError, usually saying “C object is not iterable,” where
        C is the class of the target object.
        That is why any Python sequence is iterable: they all implement __getitem__. In fact,
        the standard sequences also implement __iter__, and yours should too, because the
        special handling of __getitem__ exists for backward compatibility reasons and may be
        gone in the future
        """
        return self.words[i]

    def __len__(self):
        return len(self.words)


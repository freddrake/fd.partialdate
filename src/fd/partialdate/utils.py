"""\
Utility helpers.

These are not part of the public API.

"""

import re


class RegularExpressionGroup:

    def __init__(self, *patterns, flags=re.VERBOSE):
        self.rxs = tuple(re.compile(pattern, flags) for pattern in patterns)

    def match(self, text):
        for rx in self.rxs:
            m = rx.match(text)
            if m is not None:
                return RegularExpressionMatch(m)
        return None


class RegularExpressionMatch:

    def __init__(self, m):
        self.m = m

    def group(self, *groups):
        results = []
        for gname in groups:
            if gname in self.m.re.groupindex:
                results.append(self.m.group(gname))
            else:
                results.append(None)
        if len(groups) == 1:
            return results[0]
        else:
            return tuple(results)

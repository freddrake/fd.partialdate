"""\
Support for fd.partialdate tests.

"""

import fd.partialdate.exceptions


class AssertionHelpers:

    def assert_parse_error(self):
        return self.assertRaises(fd.partialdate.exceptions.ParseError)

    def assert_range_error(self):
        return self.assertRaises(fd.partialdate.exceptions.RangeError)

"""\
Date object that can represent partial dates: year-only, year+month,
year+month+day, month-day, or just day.

"""

import datetime
import functools
import re

import fd.partialdate.exceptions


_days_in_month = {
    1: 31,
    2: 29,  # Except for leap years; checked separately.
    3: 31,
    4: 30,
    5: 31,
    6: 30,
    7: 31,
    8: 31,
    9: 30,
    10: 31,
    11: 30,
    12: 31,
}

_re = r"""
    (?P<year>-|\d{4})
    (?:-
        (?P<month>-|\d{2})
        (?:-
            (?P<day>-|\d{2})
         )?
     )?
    $
"""
_rx = re.compile(_re, re.VERBOSE)


@functools.total_ordering
class Date:

    __slots__ = 'year', 'month', 'day', 'partial'

    def __init__(self, year=None, month=None, day=None):
        if year is None and day is None:
            if month:
                raise ValueError('must specify year or day along with month')
            else:
                raise ValueError('must specify year or day')
        if year is not None:
            if not (1 <= year <= 9999):
                raise fd.partialdate.exceptions.RangeError(
                    'year', year, 1, 9999)
        if month is None:
            if year is not None and day is not None:
                raise ValueError('cannot specify year and day without month')
            if day is not None:
                if not (1 <= day <= 31):
                    raise fd.partialdate.exceptions.RangeError(
                        'day', day, 1, 31)
        else:
            if not (1 <= month <= 12):
                raise fd.partialdate.exceptions.RangeError(
                    'month', month, 1, 12)
            if day is not None:
                dim = _days_in_month[month]
                if year and year % 4 and month == 2:
                    dim -= 1
                if not (1 <= day <= dim):
                    raise fd.partialdate.exceptions.RangeError(
                        'day', day, 1, dim)
        self.year = year
        self.month = month
        self.day = day
        # No need to check month since if month is None, at least one of
        # year or day must be None.
        self.partial = year is None or day is None

    def __repr__(self):
        cls = self.__class__
        use_keywords = False
        parts = []

        def add_arg(name, value):
            nonlocal use_keywords
            if value is None:
                use_keywords = True
            elif use_keywords:
                parts.append(f'{name}={value}')
            else:
                parts.append(str(value))

        add_arg('year', self.year)
        add_arg('month', self.month)
        add_arg('day', self.day)

        return f'{cls.__module__}.{cls.__qualname__}({", ".join(parts)})'

    def __str__(self):
        return self.isoformat()

    def __eq__(self, other):
        if isinstance(other, datetime.datetime):
            ocls = other.__class__
            raise TypeError(
                f"comparison not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")
        if isinstance(other, datetime.date):
            odata = other.year, other.month, other.day
        elif isinstance(other, Date):
            odata = other.year or 0, other.month or 0, other.day or 0
        else:
            return NotImplemented
        sdata = self.year or 0, self.month or 0, self.day or 0
        return sdata == odata

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            ocls = other.__class__
            raise TypeError(
                f"ordering not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")
        if isinstance(other, datetime.date):
            odata = other.year, other.month, other.day
            oparts = True, True, True
        elif isinstance(other, Date):
            odata = other.year or 0, other.month or 0, other.day or 0
            oparts = bool(other.year), bool(other.month), bool(other.day)
        else:
            return NotImplemented
        sparts = bool(self.year), bool(self.month), bool(self.day)
        if False in sparts or False in oparts:
            # No need to check for ValueError; every case will include
            # at least one True value since we disallow completely
            # unspecified values.
            oprecision = oparts.index(True)
            sprecision = sparts.index(True)
            if oprecision != sprecision:
                raise ValueError('ordering not supported between'
                                 ' incompatible partial dates')
        sdata = self.year or 0, self.month or 0, self.day or 0
        return sdata < odata

    def isoformat(self):
        parts = [
            (f'{self.year:04}' if self.year else '-'),
            (f'{self.month:02}' if self.month else '-'),
            (f'{self.day:02}' if self.day else '-'),
        ]
        return '-'.join(parts).rstrip('-')

    @classmethod
    def isoparse(cls, text):
        m = _rx.match(text)
        # Special case for ISO 8601 date with all components omitted.
        if m is None or text == '-----':
            raise fd.partialdate.exceptions.ParseError(
                'ISO 8601 date', text)
        year, month, day = [
            None if v in ('-', None) else int(v)
            for v in m.group('year', 'month', 'day')
        ]
        return cls(year=year, month=month, day=day)


Date.min = Date(1, 1, 1)
Date.max = Date(9999, 12, 31)

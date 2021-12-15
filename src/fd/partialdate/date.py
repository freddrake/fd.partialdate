"""\
Date object that can represent partial dates: year-only, year+month,
year+month+day, month-day, or just day.

Note that provided components must be contiguous and include the
most-significant or least-significant component; month alone cannot be
specified or omitted.

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

_re_extended = r"""
    (?P<year>\d{4})
    (?:-
        (?:
            (?:
                (?P<month>\d{2})
                -(?P<day>\d{2})
             )
            | (?P<ordinal>\d{3})
         )
     )
    $
"""

_re_basic_0 = r"""
    (?P<year>\d{4})
    (?:-
            (?P<month>\d{2})
     )?
    $
"""

_re_basic_1 = r"""
    (?P<year>-|\d{4})
    (?:
        (?:
            (?P<month>-|\d{2})
            (?P<day>\d{2})?
         )
        | (?P<ordinal>\d{3})
     )?
    $
"""
_rxs = (
    re.compile(_re_extended, re.VERBOSE),
    re.compile(_re_basic_0, re.VERBOSE),
    re.compile(_re_basic_1, re.VERBOSE),
)


def _groups(m, *groups):
    for gname in groups:
        if gname in m.re.groupindex:
            yield m.group(gname)
        else:
            yield None


@functools.total_ordering
class Date:
    """Date representation supporting partial values."""

    __slots__ = 'year', 'month', 'day', 'partial'

    def __init__(self, year=None, month=None, day=None):
        if year is None and day is None:
            if month:
                raise ValueError('must specify year or day along with month')
            else:
                raise ValueError('must specify year or day')
        if year is not None:
            if not (0 <= year <= 9999):
                raise fd.partialdate.exceptions.RangeError(
                    'year', year, 0, 9999)
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
                if year is not None and year % 4 and month == 2:
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
            odata = (
                -1 if other.year is None else other.year,
                -1 if other.month is None else other.month,
                -1 if other.day is None else other.day,
            )
        else:
            return NotImplemented
        sdata = (
            -1 if self.year is None else self.year,
            -1 if self.month is None else self.month,
            -1 if self.day is None else self.day,
        )
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
            odata = (
                -1 if other.year is None else other.year,
                -1 if other.month is None else other.month,
                -1 if other.day is None else other.day,
            )
            oparts = (
                other.year is not None,
                other.month is not None,
                other.day is not None,
            )
        else:
            return NotImplemented
        sparts = bool(self.year), bool(self.month), bool(self.day)
        sparts = (
            self.year is not None,
            self.month is not None,
            self.day is not None,
        )
        if False in sparts or False in oparts:
            # No need to check for ValueError; every case will include
            # at least one True value since we disallow completely
            # unspecified values.
            oprecision = oparts.index(True)
            sprecision = sparts.index(True)
            if oprecision != sprecision:
                raise ValueError('ordering not supported between'
                                 ' incompatible partial dates')
        sdata = (
            -1 if self.year is None else self.year,
            -1 if self.month is None else self.month,
            -1 if self.day is None else self.day,
        )
        return sdata < odata

    def isoformat(self):
        """Return an ISO 8601 formatted version of the date.

        The extended format will be used for complete dates.

        """
        parts = [
            (f'{self.year:04}' if self.year is not None else '-'),
            (f'{self.month:02}' if self.month is not None else '-'),
            (f'{self.day:02}' if self.day is not None else '-'),
        ]
        if self.month and not self.day:
            return '-'.join(parts).rstrip('-')
        if self.partial:
            return ''.join(parts).rstrip('-')
        else:
            return '-'.join(parts).rstrip('-')

    @classmethod
    def isoparse(cls, text):
        """Parse an ISO 8601 basic or extended date representation.

        Ordinal dates must include the year, and will be converted to
        year-month-day representations assuming the propleptic Gregorian
        calendar.

        """
        for rx in _rxs:
            m = rx.match(text)
            if m is not None:
                break
        else:
            raise fd.partialdate.exceptions.ParseError(
                'ISO 8601 date', text)
        year, month, day, ordinal = _groups(
            m, 'year', 'month', 'day', 'ordinal')
        if ordinal is None:
            if day is None and month == '-':
                raise fd.partialdate.exceptions.ParseError(
                    'ISO 8601 date', text)
        year, month, day, ordinal = [
            None if v in ('-', None) else int(v)
            for v in (year, month, day, ordinal)
        ]
        if ordinal is not None:
            if year is None:
                raise fd.partialdate.exceptions.ParseError(
                    'ISO 8601 date', text)
            isleap = (year % 4) == 0
            dims = sorted(_days_in_month.items())
            remaining = ordinal
            while dims:
                month, dim = dims.pop(0)
                if month == 2 and not isleap:
                    dim -= 1
                if remaining <= dim:
                    day = remaining
                    break
                remaining -= dim
            else:
                raise fd.partialdate.exceptions.RangeError(
                    'ordinal day', ordinal, 1, 365 + isleap)
        return cls(year=year, month=month, day=day)


Date.min = Date(1, 1, 1)
Date.max = Date(9999, 12, 31)

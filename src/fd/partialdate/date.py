"""\
Date objcet that can represent partial dates: year-only, year+month, as
well as year+month+date.

"""

import datetime
import functools


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


@functools.total_ordering
class Date(object):

    __slots__ = 'year', 'month', 'date'

    def __init__(self, year, month=None, day=None):
        if not (1 <= year <= 9999):
            raise ValueError('year is out of range')
        if month is None:
            if day is not None:
                raise ValueError('cannot specify day without month')
        else:
            if not (1 <= month <= 12):
                raise ValueError('year is out of range')
            if day is not None:
                # XXX Need to lookup year+month to determine range for day.
                if not (1 <= day <= _days_in_month[month]):
                    raise ValueError('day is out of range')
        self.year = year
        # We use integers here to avoid cross-type comparisons when sorting.
        self.month = month or 0
        self.day = day or 0

    def __repr__(self):
        cls = self.__class__
        clsname = getattr(cls, '__qualname__', cls.__name__)
        clsname = cls.__module__ + '.' + clsname
        repr = clsname + '(' + str(self.year)
        if self.month:
            repr += ', ' + str(self.month)
            if self.day:
                repr += ', ' + str(self.day)
        return repr + ')'

    def __str__(self):
        if self.month:
            if self.day:
                return '%04d-%02d-%02' % (self.year, self.month, self.day)
            else:
                return '%04d-%02d' % (self.year, self.month)
        else:
            return '%04d' % self.year

    def __eq__(self, other):
        if isinstance(other, datetime.datetime):
            return NotImplemented
        if isinstance(other, datetime.date):
            odata = other.year, other.month, other.day
        elif isinstance(other, Date):
            odata = other.year, other.month, other.day
        else:
            return NotImplemented
        sdata = self.year, self.month, self.day
        return sdata == odata

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            return NotImplemented
        if isinstance(other, datetime.date):
            odata = other.year, other.month, other.day
        elif isinstance(other, Date):
            odata = other.year, other.month, other.day
        else:
            return NotImplemented
        sdata = self.year, self.month, self.day
        return sdata < odata

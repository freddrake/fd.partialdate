"""\
Time object that can represent partial times: hour-only, hour+minute,
hour+minute+second, minute+second, or just second.

Sub-second resolutions are not supported.

Note that provided components must be contiguous and include the
most-significant or least-significant component; minutes alone cannot be
specified or omitted.

"""

import datetime
import functools
import re

import fd.partialdate.exceptions


_re = r"""
    (?P<hour>-|\d{2})
    (?:
        (?P<minute>-|\d{2})
        (?:
            (?P<second>-|\d{2})
         )?
     )?
    $
"""
_rx = re.compile(_re, re.VERBOSE)


@functools.total_ordering
class Time:

    __slots__ = 'hour', 'minute', 'second', 'partial'

    def __init__(self, hour=None, minute=None, second=None):
        if hour is None and second is None:
            if minute:
                raise ValueError(
                    'must specify hour or second along with minute')
            else:
                raise ValueError('must specify hour or second')
        if hour is not None:
            if not (0 <= hour <= 23):
                raise fd.partialdate.exceptions.RangeError(
                    'hour', hour, 0, 23)
        if minute is None:
            if hour is not None and second is not None:
                raise ValueError(
                    'cannot specify hour and second without minute')
            if second is not None:
                if not (0 <= second <= 59):
                    raise fd.partialdate.exceptions.RangeError(
                        'second', second, 0, 59)
        else:
            if not (0 <= minute <= 59):
                raise fd.partialdate.exceptions.RangeError(
                    'minute', minute, 0, 59)
            if second is not None:
                if not (0 <= second <= 59):
                    raise fd.partialdate.exceptions.RangeError(
                        'second', second, 0, 59)
        self.hour = hour
        self.minute = minute
        self.second = second
        # No need to check minute since if minute is None, at least one of
        # hour or second must be None.
        self.partial = hour is None or second is None

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

        add_arg('hour', self.hour)
        add_arg('minute', self.minute)
        add_arg('second', self.second)

        return f'{cls.__module__}.{cls.__qualname__}({", ".join(parts)})'

    def __eq__(self, other):
        if isinstance(other, datetime.datetime):
            ocls = other.__class__
            raise TypeError(
                f"comparison not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")
        if isinstance(other, datetime.time):
            odata = other.hour, other.minute, other.second, other.microsecond
        elif isinstance(other, Time):
            odata = (
                -1 if other.hour is None else other.hour,
                -1 if other.minute is None else other.minute,
                -1 if other.second is None else other.second,
                0
            )
        else:
            return NotImplemented
        sdata = (
            -1 if self.hour is None else self.hour,
            -1 if self.minute is None else self.minute,
            -1 if self.second is None else self.second,
            0
        )
        return sdata == odata

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            ocls = other.__class__
            raise TypeError(
                f"ordering not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")
        if isinstance(other, datetime.time):
            odata = other.hour, other.minute, other.second, other.microsecond
            oparts = True, True, True, True
        elif isinstance(other, Time):
            odata = (
                -1 if other.hour is None else other.hour,
                -1 if other.minute is None else other.minute,
                -1 if other.second is None else other.second,
                0
            )
            oparts = (
                other.hour is not None,
                other.minute is not None,
                other.second is not None,
                True,
            )
        else:
            return NotImplemented
        sparts = (
            self.hour is not None,
            self.minute is not None,
            self.second is not None,
            True,
        )
        if False in sparts or False in oparts:
            # No need to check for ValueError; every case will include
            # at least one True value since we disallow completely
            # unspecified values.
            oprecision = oparts.index(True)
            sprecision = sparts.index(True)
            if oprecision != sprecision:
                raise ValueError('ordering not supported between'
                                 ' incompatible partial times')
        sdata = (
            -1 if self.hour is None else self.hour,
            -1 if self.minute is None else self.minute,
            -1 if self.second is None else self.second,
            0
        )
        return sdata < odata

    def isoformat(self):
        parts = [
            (f'{self.hour:02}' if self.hour is not None else '-'),
            (f'{self.minute:02}' if self.minute is not None else '-'),
            (f'{self.second:02}' if self.second is not None else '-'),
        ]
        return ''.join(parts).rstrip('-')

    @classmethod
    def isoparse(cls, text):
        m = _rx.match(text)
        # Special case for ISO 8601 date with all components omitted.
        if m is None or text == '---':
            raise fd.partialdate.exceptions.ParseError(
                'ISO 8601 time', text)
        hour, minute, second = [
            None if v in ('-', None) else int(v)
            for v in m.group('hour', 'minute', 'second')
        ]
        return cls(hour=hour, minute=minute, second=second)

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
import typing

import fd.partialdate.exceptions
import fd.partialdate.utils


_re_basic = r"""
    (?P<hour>-|\d{2})
    (?:
        (?P<minute>-|\d{2})
        (?:
            (?P<second>\d{2})
         )?
     )?
    # Not implemented:  (?:[,.](?P<fractional>\d{1,6}))
    (?P<tzinfo>[zZ]|[-+]\d{2}|[-+]\d{4})?
    $
"""

_re_extended = r"""
    (?P<hour>\d{2})
    :(?P<minute>\d{2})
    :(?P<second>\d{2})
    # Not implemented:  (?:[,.](?P<fractional>\d{1,6}))
    (?P<tzinfo>[zZ]|[-+]\d{2}|[-+]\d{2}:\d{2})?
    $
"""
_rx = fd.partialdate.utils.RegularExpressionGroup(
    _re_extended,
    _re_basic,
    flags=re.VERBOSE,
)


def _tzstr(tzinfo, sep):
    if tzinfo is None:
        return ''
    seconds = int(tzinfo.utcoffset(None).total_seconds())
    if seconds < 0:
        seconds = -seconds
        sign = '-'
    else:
        sign = '+'
    minutes = seconds // 60
    hours = minutes // 60
    minutes = minutes - (hours * 60)
    seconds = seconds - (hours * 60 * 60) - (minutes * 60)
    assert seconds == 0
    if hours == minutes == 0:
        return 'Z'
    else:
        return f'{sign}{hours:02}{sep}{minutes:02}'


@functools.total_ordering
class Time:
    """Date representation supporting partial values."""

    __slots__ = 'hour', 'minute', 'second', 'tzinfo', 'partial'

    hour: typing.Optional[int]
    """Hour of day, or ``None``."""

    minute: typing.Optional[int]
    """Minute of hour, or ``None``."""

    second: typing.Optional[int]
    """Second of minute, or ``None``."""

    tzinfo: typing.Optional[datetime.timezone]
    """Timezone applied to time, or ``None`` for local time."""

    partial: bool
    """Indicates whether the value is partial (``True``) or complete."""

    def __init__(self, hour=None, minute=None, second=None, tzinfo=None):
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
        self.tzinfo = tzinfo
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
                parts.append(f'{name}={value!r}')
            else:
                parts.append(repr(value))

        add_arg('hour', self.hour)
        add_arg('minute', self.minute)
        add_arg('second', self.second)
        add_arg('tzinfo', self.tzinfo)

        return f'{cls.__module__}.{cls.__qualname__}({", ".join(parts)})'

    def __eq__(self, other):
        if isinstance(other, datetime.datetime):
            ocls = other.__class__
            raise TypeError(
                f"comparison not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")
        if isinstance(other, datetime.time):
            odata = (
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
                other.tzinfo,
            )
        elif isinstance(other, Time):
            odata = (
                -1 if other.hour is None else other.hour,
                -1 if other.minute is None else other.minute,
                -1 if other.second is None else other.second,
                0,
                other.tzinfo,
            )
        else:
            return NotImplemented

        if self.tzinfo != other.tzinfo:
            opartial = getattr(other, 'partial', False)
            if self.partial or opartial:
                if self.partial and opartial:
                    extra = ''
                else:
                    extra = ' and complete'
                raise TypeError(
                    f"can't compare partial{extra} time values"
                    f" with different time zones")

            # Values are complete; timezones differ.  Let datetime
            # figure out equality.
            lh = datetime.time(
                hour=self.hour, minute=self.minute, second=self.second,
                microsecond=0, tzinfo=self.tzinfo)
            rh = datetime.time(
                hour=other.hour, minute=other.minute, second=other.second,
                microsecond=odata[-2], tzinfo=other.tzinfo)
            return lh == rh

        sdata = (
            -1 if self.hour is None else self.hour,
            -1 if self.minute is None else self.minute,
            -1 if self.second is None else self.second,
            0,
            self.tzinfo,
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
            odata = (
                other.hour,
                other.minute,
                other.second,
                other.microsecond,
                other.tzinfo,
            )
            oparts = True, True, True, True
        elif isinstance(other, Time):
            odata = (
                -1 if other.hour is None else other.hour,
                -1 if other.minute is None else other.minute,
                -1 if other.second is None else other.second,
                0,
                other.tzinfo,
            )
            oparts = (
                other.hour is not None,
                other.minute is not None,
                other.second is not None,
                True,
            )
        else:
            return NotImplemented

        tzinfos = [tz for tz in (self.tzinfo, other.tzinfo) if tz is not None]
        if len(tzinfos) == 1:
            # Referring to offset is odd, but mirrors a similar message
            # from the standard library's datetime implementation.
            raise TypeError(
                "can't order offset-naive and offset-aware time values")

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

        if tzinfos and tzinfos[0] != tzinfos[1]:
            assert len(tzinfos) == 2
            opartial = getattr(other, 'partial', False)
            if self.partial or opartial:
                if self.partial and opartial:
                    extra = ''
                else:
                    extra = ' and complete'
                raise TypeError(
                    f"can't order partial{extra} time values"
                    f" with different time zones")
            # Values are complete; timezones differ.  Let datetime
            # figure out the order.
            lh = datetime.time(
                hour=self.hour, minute=self.minute, second=self.second,
                tzinfo=self.tzinfo)
            rh = datetime.time(
                hour=other.hour, minute=other.minute, second=other.second,
                tzinfo=other.tzinfo)
            return lh < rh

        sdata = (
            -1 if self.hour is None else self.hour,
            -1 if self.minute is None else self.minute,
            -1 if self.second is None else self.second,
            0,
            self.tzinfo,
        )
        return sdata < odata

    def isoformat(self, extended=True):
        """Return an ISO 8601 formatted version of the date.

        :param extended:
            Prefer the extended format, if applicable for the value.

        The extended format will be preferred for complete times; the
        basic format will always be used for partial values.

        """
        parts = [
            (f'{self.hour:02}' if self.hour is not None else '-'),
            (f'{self.minute:02}' if self.minute is not None else '-'),
            (f'{self.second:02}' if self.second is not None else '-'),
        ]
        while parts[-1] == '-':
            del parts[-1]
        if self.hour is None or self.minute is None or not extended:
            sep = ''
        else:
            sep = ':'
        return sep.join(parts) + _tzstr(self.tzinfo, sep)

    @classmethod
    def isoparse(cls, text: str):
        """Parse an ISO 8601 basic time representation.

        :param text:  ISO 8601 representation to convert

        """
        m = _rx.match(text)
        # Special case for ISO 8601 time with all components omitted.
        if m is None:
            raise fd.partialdate.exceptions.ParseError(
                'ISO 8601 time', text)
        hour, minute, second = [
            None if v in ('-', None) else int(v)
            for v in m.group('hour', 'minute', 'second')
        ]
        tzinfo = m.group('tzinfo')
        if tzinfo is None:
            pass
        elif tzinfo in ('z', 'Z'):
            tzinfo = datetime.timezone.utc
        elif len(tzinfo) == 3:
            if tzinfo in ('-00', '+00'):
                tzinfo = datetime.timezone.utc
            else:
                offset = datetime.timedelta(hours=int(tzinfo))
                tzinfo = datetime.timezone(offset)
        else:
            if ':' in tzinfo:
                tzinfo = tzinfo.replace(':', '')
            assert len(tzinfo) == 5, repr(tzinfo)
            if tzinfo in ('-0000', '+0000'):
                tzinfo = datetime.timezone.utc
            else:
                hours = int(tzinfo[1:3])
                minutes = int(tzinfo[3:])
                offset = datetime.timedelta(hours=hours, minutes=minutes)
                if tzinfo[0] == '-':
                    offset = -offset
                tzinfo = datetime.timezone(offset)
        return cls(hour=hour, minute=minute, second=second, tzinfo=tzinfo)

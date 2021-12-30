"""\
Datetime object that can represent partial datetimes.

Sub-second resolutions are not supported.

"""

import datetime
import functools
import typing

import fd.partialdate.date
import fd.partialdate.exceptions
import fd.partialdate.time
import fd.partialdate.utils


_re_basic = r"""
    (?P<year>-|\d{4})
    (?:
        (?:
            (?P<month>-|\d{2})
            (?P<day>\d{2})?
         )
        | (?P<ordinal>\d{3})
     )?
    (?:T|t|\ )
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
    (?:T|t|\ )
    (?P<hour>\d{2})
    :(?P<minute>\d{2})
    (?:
        :(?P<second>\d{2})
     )?
    # Not implemented:  (?:[,.](?P<fractional>\d{1,6}))
    (?P<tzinfo>[zZ]|[-+]\d{2}|[-+]\d{2}:\d{2})?
    $
"""
_rx = fd.partialdate.utils.RegularExpressionGroup(
    _re_extended,
    _re_basic,
)


@functools.total_ordering
class Datetime:
    """Datetime representation supporting partial values."""

    __slots__ = ('_date', '_time', 'partial')

    partial: bool
    """Indicates whether the value is partial (``True``) or complete."""

    def __init__(self, year=None, month=None, day=None,
                 hour=None, minute=None, second=None, tzinfo=None):
        self._date = fd.partialdate.date.Date(year, month, day)
        self._time = fd.partialdate.time.Time(hour, minute, second, tzinfo)
        self.partial = self._date.partial or self._time.partial

    @property
    def year(self) -> typing.Optional[int]:
        """Calendar year, or ``None``."""
        return self._date.year

    @property
    def month(self) -> typing.Optional[int]:
        """Calendar month, or ``None``."""
        return self._date.month

    @property
    def day(self) -> typing.Optional[int]:
        """Calendar day, or ``None``."""
        return self._date.day

    @property
    def hour(self) -> typing.Optional[int]:
        """Hour of day, or ``None``."""
        return self._time.hour

    @property
    def minute(self) -> typing.Optional[int]:
        """Minute of hour, or ``None``."""
        return self._time.minute

    @property
    def second(self) -> typing.Optional[int]:
        """Second of minute, or ``None``."""
        return self._time.second

    @property
    def tzinfo(self) -> typing.Optional[datetime.timezone]:
        """Timezone applied to time, or ``None`` for local time."""
        return self._time.tzinfo

    def __repr__(self) -> str:
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

        add_arg('year', self.year)
        add_arg('month', self.month)
        add_arg('day', self.day)
        add_arg('hour', self.hour)
        add_arg('minute', self.minute)
        add_arg('second', self.second)
        add_arg('tzinfo', self.tzinfo)

        return f'{cls.__module__}.{cls.__qualname__}({", ".join(parts)})'

    def __eq__(self, other):
        if isinstance(other, datetime.datetime):
            d = other.date()
            t = other.time().replace(tzinfo=other.tzinfo)
            opartial = False
        elif isinstance(other, Datetime):
            d = other._date
            t = other._time
            opartial = other.partial
        else:
            return NotImplemented

        if self.tzinfo != other.tzinfo:
            if self.partial or opartial:
                # return False
                if self.partial and opartial:
                    extra = ''
                else:
                    extra = ' and complete'
                raise TypeError(
                    f"can't compare partial{extra} datetime values"
                    f" with different time zones")

            # Values are complete; timezones differ.  Let datetime
            # figure out equality.
            lh = datetime.datetime(
                year=self.year, month=self.month, day=self.day,
                hour=self.hour, minute=self.minute, second=self.second,
                microsecond=0, tzinfo=self.tzinfo)
            rh = datetime.datetime(
                year=other.year, month=other.month, day=other.day,
                hour=other.hour, minute=other.minute, second=other.second,
                microsecond=getattr(other, 'microsecond', 0),
                tzinfo=other.tzinfo)
            return lh == rh

        return self._date == d and self._time == t

    def __lt__(self, other):
        if isinstance(other, datetime.datetime):
            d = other.date()
            t = other.time().replace(tzinfo=other.tzinfo)
            opartial = False
        elif isinstance(other, Datetime):
            d = other._date
            t = other._time
            opartial = other.partial
        else:
            ocls = other.__class__
            raise TypeError(
                f"ordering not supported between instances of"
                f" '{self.__class__.__name__}' and"
                f" '{ocls.__module__}.{ocls.__qualname__}'")

        # Could let this fall through to the datetime comparison below,
        # but we want to control the message for consistency.
        tzinfos = [tz for tz in (self.tzinfo, other.tzinfo) if tz is not None]
        if len(tzinfos) == 1:
            # Referring to offset is odd, but mirrors a similar message
            # from the standard library's datetime implementation.
            raise TypeError(
                "can't order offset-naive and offset-aware datetime values")

        if self.tzinfo != other.tzinfo:
            if self.partial or opartial:
                if self.partial and opartial:
                    extra = ''
                else:
                    extra = ' and complete'
                raise TypeError(
                    f"can't order partial{extra} datetime values"
                    f" with different time zones")

            # Values are complete; timezones differ.  Let datetime
            # figure out equality.
            lh = datetime.datetime(
                year=self.year, month=self.month, day=self.day,
                hour=self.hour, minute=self.minute, second=self.second,
                microsecond=0, tzinfo=self.tzinfo)
            rh = datetime.datetime(
                year=other.year, month=other.month, day=other.day,
                hour=other.hour, minute=other.minute, second=other.second,
                microsecond=getattr(other, 'microsecond', 0),
                tzinfo=other.tzinfo)
            return lh < rh

        if self._date < d:
            return True
        elif self._date == d:
            return self._time < t
        else:
            return False

    def __str__(self) -> str:
        return self.isoformat(sep=' ')

    def isoformat(self, sep='T', extended=True) -> str:
        """Return an ISO 8601 formatted version of the datetime.

        :param sep:
            Separator to use between date and time.  Most common
            alternative is a space.
        :param extended:
            Prefer the extended format, if applicable for the value.

        The extended format will be preferred for complete values; the
        basic format will always be used for partial values.

        """
        if self._date.partial:
            extended = False
        time = self._time.isoformat(extended=extended)
        if extended:
            extended = ':' in time
        date = self._date.isoformat(extended=extended)
        return f'{date}{sep}{time}'

    @classmethod
    def isoparse(cls, text: str):
        """Parse an ISO 8601 basic or extended date representation.

        :param text:  ISO 8601 representation to convert

        Ordinal dates must include the year, and will be converted to
        year-month-day representations assuming the proleptic Gregorian
        calendar.

        """
        m = _rx.match(text)
        if m is None:
            raise fd.partialdate.exceptions.ParseError(
                'ISO 8601 datetime', text)
        year, month, day, ordinal = m.group('year', 'month', 'day', 'ordinal')
        hour, minute, second = m.group('hour', 'minute', 'second')
        if ordinal is None:
            if day is None and month == '-':
                raise fd.partialdate.exceptions.ParseError(
                    'ISO 8601 datetime', text)
        year, month, day, ordinal, hour, minute, second = [
            None if v in ('-', None) else int(v)
            for v in (year, month, day, ordinal, hour, minute, second)
        ]
        if ordinal is not None:
            month, day = fd.partialdate.date._ordinal2md(
                'ISO 8601 datetime', text, year, ordinal)
        tzinfo = fd.partialdate.time._tzinfo(m.group('tzinfo'))
        return cls(year=year, month=month, day=day,
                   hour=hour, minute=minute, second=second,
                   tzinfo=tzinfo)

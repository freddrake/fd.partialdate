"""\
Exceptions defined for :mod:`fd.partialdate`.

"""


class PartialdateException(Exception):
    """Base class for exceptions defined in :mod:`fd.partialdate`."""

    message: str
    """User-facing message describing the error."""

    def __init__(self, message: str):
        super(PartialdateException, self).__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class ParseError(PartialdateException, ValueError):

    what: str
    """Identifier of what was being parsed (example: ``'ISO 8601 date'``)."""

    value: str
    """Unparsable value."""

    def __init__(self, what: str, value: int):
        self.what = what
        self.value = value
        super(ParseError, self).__init__(
            f'text cannot be parsed as an {what}: {value!r}')


class RangeError(PartialdateException, ValueError):

    field: str
    """Name of the input fields that's outside the allowed range."""

    value: int
    """Provided value of the field."""

    min: int
    """Minimum allowed value in the range."""

    max: int
    """Maximum allowed value in the range."""

    def __init__(self, field: str, value: int, min: int, max: int):
        self.field = field
        self.value = value
        self.min = min
        self.max = max
        super(RangeError, self).__init__(
            f'{field} is out of range [{min}..{max}]: {value}')

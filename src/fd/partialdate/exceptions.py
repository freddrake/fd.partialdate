"""\
Exceptions defined for :mod:`fd.partialdate`.

"""


class ParseError(ValueError):

    message: str
    """User-facing message describing the error."""

    what: str
    """Identifier of what was being parsed (example: ``'ISO 8601 date'``)."""

    value: str
    """Unparsable value."""

    def __init__(self, what: str, value: str):
        self.what = what
        self.value = value
        self.message = f'text cannot be parsed as an {what}: {value!r}'
        super(ParseError, self).__init__(what, value)

    def __str__(self):
        return self.message


class RangeError(ValueError):

    field: str
    """Name of the input fields that's outside the allowed range."""

    message: str
    """User-facing message describing the error."""

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
        self.message = f'{field} is out of range [{min}..{max}]: {value}'
        super(RangeError, self).__init__(field, value, min, max)

    def __str__(self):
        return self.message

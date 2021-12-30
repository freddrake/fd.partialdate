=====================================================
fd.partialdate - library for partial date/time values
=====================================================

**fd.partialdate** is a library for representing and serializing
possibly partial dates and times, where missing portions may be omitted
at either the least-significant or most-significant bits.  (For example,
a date might include just the year, the year and month, or the month and
day, but will never be the year and day without the month.)

Parsing supports both the basic and extended formats from ISO 8601.
Serialization uses the extended formats where possible, falling back to
the basic format where not.  Callers can request that the basic format
always be used.


Release history
---------------

No public release.

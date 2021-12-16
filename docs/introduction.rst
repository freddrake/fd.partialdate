Introduction
============

The ``fd.partialdate`` library supports incomplete date & time values
and serialization using ISO 8601 formats.

The ISO 8601 formats listed below are supported for both parsing and
serialization.


Supported date formats
----------------------


Basic date format
~~~~~~~~~~~~~~~~~

| YYYYMMDD
| YYYY-MM
| YYYY
| YYYYDDD


Basic date format (partial values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| -MMDD
| --DD
| -MM
| -DDD


Extended date format
~~~~~~~~~~~~~~~~~~~~

| YYYY-MM-DD
| YYYY-DDD


Supported time formats
----------------------

Basic time format
~~~~~~~~~~~~~~~~~

| hhmmss
| hhmmssZ
| hhmmss±hh
| hhmmss±hhmm
| hhmm
| hhmmZ
| hhmm±hh
| hhmm±hhmm
| hh
| hhZ
| hh±hh
| hh±hhmm


Basic time format (partial values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| -mmss
| -mmssZ
| -mmss±hh
| -mmss±hhmm
| -mm
| -mmZ
| -mm±-
| -mm±hhmm
| --ss
| --ssZ
| --ss±hh
| --ss±hhmm


Extended time format
~~~~~~~~~~~~~~~~~~~~

| hh:mm:ss
| hh:mm:ssZ
| hh:mm:ss±hh
| hh:mm:ss±hh:mm
| hh:mm
| hh:mmZ
| hh:mm±hh
| hh:mm±hh:mm

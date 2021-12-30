Introduction
============

The ``fd.partialdate`` library supports incomplete date & time values
and serialization using ISO 8601 formats.

The ISO 8601 formats listed below are supported for both parsing and
serialization.

Where applicable, the ``T`` time indicator and the ``Z`` UTC indicator
are accepted in both upper- and lower-case.  The ``T`` time indicator
can also be replaced with a single space character.


Supported date formats
----------------------


Basic format
~~~~~~~~~~~~

| YYYYMMDD
| YYYYDDD


Basic format (partial values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| YYYY-MM
| YYYY
| -MMDD
| --DD
| -MM
| -DDD


Extended format
~~~~~~~~~~~~~~~

| YYYY-MM-DD
| YYYY-DDD


Supported time formats
----------------------

Basic format
~~~~~~~~~~~~

| hhmmss
| hhmmssZ
| hhmmss±hh
| hhmmss±hhmm


Basic format (partial values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| hhmm
| hhmmZ
| hhmm±hh
| hhmm±hhmm
| hh
| hhZ
| hh±hh
| hh±hhmm
| -mmss
| -mmssZ
| -mmss±hh
| -mmss±hhmm
| -mm
| -mmZ
| -mm±-hh
| -mm±hhmm
| --ss
| --ssZ
| --ss±hh
| --ss±hhmm


Extended format
~~~~~~~~~~~~~~~

| hh:mm:ss
| hh:mm:ssZ
| hh:mm:ss±hh
| hh:mm:ss±hh:mm


Extended format (partial values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| hh:mm
| hh:mmZ
| hh:mm±hh
| hh:mm±hh:mm


Supported datetime formats
--------------------------


Basic format
~~~~~~~~~~~~

| YYYYMMDDThhmmss
| YYYYMMDDThhmmssZ
| YYYYMMDDThhmmss±hh
| YYYYMMDDThhmmss±hhmm
| YYYYDDDThhmmss
| YYYYDDDThhmmssZ
| YYYYDDDThhmmss±hh
| YYYYDDDThhmmss±hhmm


Basic format (partial date values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| YYYYMMThhmmss
| YYYYMMThhmmssZ
| YYYYMMThhmmss±hh
| YYYYMMThhmmss±hhmm
| YYYYThhmmss
| YYYYThhmmssZ
| YYYYThhmmss±hh
| YYYYThhmmss±hhmm
| -MMDDThhmmss
| -MMDDThhmmssZ
| -MMDDThhmmss±hh
| -MMDDThhmmss±hhmm
| --DDThhmmss
| --DDThhmmssZ
| --DDThhmmss±hh
| --DDThhmmss±hhmm


Basic format (partial time values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| YYYYMMDDThhmm
| YYYYMMDDThhmmZ
| YYYYMMDDThhmm±hh
| YYYYMMDDThhmm±hhmm
| YYYYMMDDThh
| YYYYMMDDThhZ
| YYYYMMDDThh±hh
| YYYYMMDDThh±hhmm
| YYYYDDDThhmm
| YYYYDDDThhmmZ
| YYYYDDDThhmm±hh
| YYYYDDDThhmm±hhmm
| YYYYDDDThh
| YYYYDDDThhZ
| YYYYDDDThh±hh
| YYYYDDDThh±hhmm


Basic format (partial date & time values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| -MMDDThhmm
| -MMDDThhmmZ
| -MMDDThhmm±hh
| -MMDDThhmm±hhmm
| --DDTThh
| --DDTThhZ
| --DDTThh±hh
| --DDTThh±hhmm


Extended format
~~~~~~~~~~~~~~~

| YYYY-MM-DDThh:mm:ss
| YYYY-MM-DDThh:mm:ssZ
| YYYY-MM-DDThh:mm:ss±hh
| YYYY-MM-DDThh:mm:ss±hhmm
| YYYY-DDDThh:mm:ss
| YYYY-DDDThh:mm:ssZ
| YYYY-DDDThh:mm:ss±hh
| YYYY-DDDThh:mm:ss±hhmm


Extended format (partial time values)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

| YYYY-MM-DDThh:mm
| YYYY-MM-DDThh:mmZ
| YYYY-MM-DDThh:mm±hh
| YYYY-MM-DDThh:mm±hhmm
| YYYY-DDDThh:mm
| YYYY-DDDThh:mmZ
| YYYY-DDDThh:mm±hh
| YYYY-DDDThh:mm±hhmm

"""\
Support for fd.partialdate tests.

"""

import fd.partialdate.exceptions


class AssertionHelpers:

    def assert_parse_error(self):
        return self.assertRaises(fd.partialdate.exceptions.ParseError)

    def assert_range_error(self):
        return self.assertRaises(fd.partialdate.exceptions.RangeError)


class DateRangeChecks:

    def test_year_range_check(self):
        for bad_year in (-42, -2, -1, 10000, 424242):
            with self.assert_range_error() as cm:
                self.factory(year=bad_year)
            message = str(cm.exception)
            self.assertIn('year is out of range [0..9999]', message)

    def test_month_range_check(self):
        for bad_month in (-42, -1, 0, 13, 42, 10000):
            with self.assert_range_error() as cm:
                self.factory(year=2021, month=bad_month)
            message = str(cm.exception)
            self.assertIn('month is out of range [1..12]', message)

    def test_day_range_check_fully_specified(self):
        for bad_day in (-42, -1, 0, 32, 42, 10000):
            with self.assert_range_error() as cm:
                self.factory(year=2021, month=12, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..31]', message)

    def test_day_range_check_february_leap_years(self):
        for year in (0, 4, 1992, 2000, 2004, 2016, 2020, 2024, 9996):
            date = self.factory(year, 2, 28)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 28)

            date = self.factory(year, 2, 29)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 29)

            for bad_day in (-42, -1, 0, 30, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    self.factory(year=year, month=2, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..29]', message)

    def test_day_range_check_february_non_leap_years(self):
        for year in (1, 1989, 1997, 2001, 2013, 2017, 2021, 9993,
                     2, 1990, 1998, 2002, 2014, 2018, 2022, 9994,
                     2, 1991, 1999, 2003, 2015, 2019, 2023, 9995):
            date = self.factory(year, 2, 28)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 28)

            for bad_day in (-42, -1, 0, 29, 30, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    self.factory(year=year, month=2, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..28]', message)

    def test_day_range_check_february_unspecified_years(self):
        date = self.factory(None, 2, 28)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 28)

        date = self.factory(None, 2, 29)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 29)

        for bad_day in (-42, -1, 0, 30, 31, 32, 42, 10000):
            with self.assert_range_error() as cm:
                self.factory(year=None, month=2, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..29]', message)

    def test_day_range_check_30day_months(self):
        for month in (4, 6, 9, 11):
            date = self.factory(None, month, 30)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, month)
            self.assertEqual(date.day, 30)

            for bad_day in (-42, -1, 0, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    self.factory(
                        year=None, month=month, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..30]', message)

    def test_day_range_check_31day_months(self):
        for month in (1, 3, 5, 7, 8, 10, 12):
            date = self.factory(None, month, 31)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, month)
            self.assertEqual(date.day, 31)

            for bad_day in (-42, -1, 0, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    self.factory(
                        year=None, month=month, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..31]', message)

    def test_day_range_check_unspecified_year_month(self):
        for day in (1, 28, 29, 30, 31):
            date = self.factory(None, None, day)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, None)
            self.assertEqual(date.day, day)

        for bad_day in (-42, -1, 0, 32, 42, 10000):
            with self.assert_range_error() as cm:
                self.factory(year=None, month=None, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..31]', message)


class TimeRangeChecks:

    def test_hour_range_check(self):
        for bad_hour in (-42, -2, -1, 24, 25, 10000, 424242):
            with self.assert_range_error() as cm:
                fd.partialdate.time.Time(hour=bad_hour)
            message = str(cm.exception)
            self.assertIn('hour is out of range [0..23]', message)

    def test_minute_range_check(self):
        for bad_minute in (-42, -2, -1, 60, 61, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.time.Time(hour=21, minute=bad_minute)
            message = str(cm.exception)
            self.assertIn('minute is out of range [0..59]', message)

    def test_second_range_check_fully_specified(self):
        for bad_second in (-42, -2, -1, 60, 61, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.time.Time(hour=21, minute=12,
                                         second=bad_second)
            message = str(cm.exception)
            self.assertIn('second is out of range [0..59]', message)

    def test_second_range_check_unspecified_hour(self):
        for minute in (1, 3, 5, 7, 8, 10, 12):
            time = fd.partialdate.time.Time(None, minute, 59)
            self.assertEqual(time.hour, None)
            self.assertEqual(time.minute, minute)
            self.assertEqual(time.second, 59)

            for bad_second in (-42, -2, -1, 60, 61, 10000):
                with self.assert_range_error() as cm:
                    fd.partialdate.time.Time(
                        hour=None, minute=minute, second=bad_second)
                message = str(cm.exception)
                self.assertIn('second is out of range [0..59]', message)

    def test_second_range_check_unspecified_hour_minute(self):
        for second in (1, 30, 31, 59):
            time = fd.partialdate.time.Time(None, None, second)
            self.assertEqual(time.hour, None)
            self.assertEqual(time.minute, None)
            self.assertEqual(time.second, second)

        for bad_second in (-42, -2, -1, 60, 61, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.time.Time(hour=None, minute=None,
                                         second=bad_second)
            message = str(cm.exception)
            self.assertIn('second is out of range [0..59]', message)

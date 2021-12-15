"""\
Tests for fd.partialdate.date.

"""

import datetime
import unittest

import fd.partialdate.date
import tests.utils


class DateTestCase(tests.utils.AssertionHelpers, unittest.TestCase):

    def test_ymd_construction(self):
        date = fd.partialdate.date.Date(0, 12, 6)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 6)
        self.assertFalse(date.partial)
        self.assertEqual(date.isoformat(), '0000-12-06')
        self.assertEqual(str(date), '0000-12-06')

        date = fd.partialdate.date.Date(2021, 12, 6)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 6)
        self.assertFalse(date.partial)
        self.assertEqual(date.isoformat(), '2021-12-06')
        self.assertEqual(str(date), '2021-12-06')

    def test_ym_construction(self):
        date = fd.partialdate.date.Date(0, 12)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000-12')
        self.assertEqual(str(date), '0000-12')

        date = fd.partialdate.date.Date(2021, 12)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021-12')
        self.assertEqual(str(date), '2021-12')

    def test_y_construction(self):
        date = fd.partialdate.date.Date(0)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000')
        self.assertEqual(str(date), '0000')

        date = fd.partialdate.date.Date(2021)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021')
        self.assertEqual(str(date), '2021')

    def test_md_construction(self):
        date = fd.partialdate.date.Date(month=12, day=8)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '-1208')
        self.assertEqual(str(date), '-1208')

    def test_d_construction(self):
        date = fd.partialdate.date.Date(day=8)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '--08')
        self.assertEqual(str(date), '--08')

    def test_yd_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.date.Date(0, day=6)
        self.assertEqual(str(cm.exception),
                         'cannot specify year and day without month')

        with self.assertRaises(ValueError) as cm:
            fd.partialdate.date.Date(2021, day=6)
        self.assertEqual(str(cm.exception),
                         'cannot specify year and day without month')

    def test_m_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.date.Date(month=12)
        self.assertEqual(str(cm.exception),
                         'must specify year or day along with month')

    def test_empty_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.date.Date()
        self.assertEqual(str(cm.exception),
                         'must specify year or day')

    def test_year_range_check(self):
        for bad_year in (-42, -2, -1, 10000, 424242):
            with self.assert_range_error() as cm:
                fd.partialdate.date.Date(year=bad_year)
            message = str(cm.exception)
            self.assertIn('year is out of range [0..9999]', message)

    def test_month_range_check(self):
        for bad_month in (-42, -1, 0, 13, 42, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.date.Date(year=2021, month=bad_month)
            message = str(cm.exception)
            self.assertIn('month is out of range [1..12]', message)

    def test_day_range_check_fully_specified(self):
        for bad_day in (-42, -1, 0, 32, 42, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.date.Date(year=2021, month=12, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..31]', message)

    def test_day_range_check_february_leap_years(self):
        for year in (0, 4, 1992, 2000, 2004, 2016, 2020, 2024, 9996):
            date = fd.partialdate.date.Date(year, 2, 28)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 28)

            date = fd.partialdate.date.Date(year, 2, 29)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 29)

            for bad_day in (-42, -1, 0, 30, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date(year=year, month=2, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..29]', message)

    def test_day_range_check_february_non_leap_years(self):
        for year in (1, 1989, 1997, 2001, 2013, 2017, 2021, 9993,
                     2, 1990, 1998, 2002, 2014, 2018, 2022, 9994,
                     2, 1991, 1999, 2003, 2015, 2019, 2023, 9995):
            date = fd.partialdate.date.Date(year, 2, 28)
            self.assertEqual(date.year, year)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 28)

            for bad_day in (-42, -1, 0, 29, 30, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date(year=year, month=2, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..28]', message)

    def test_day_range_check_february_unspecified_years(self):
        date = fd.partialdate.date.Date(None, 2, 28)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 28)

        date = fd.partialdate.date.Date(None, 2, 29)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 2)
        self.assertEqual(date.day, 29)

        for bad_day in (-42, -1, 0, 30, 31, 32, 42, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.date.Date(year=None, month=2, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..29]', message)

    def test_day_range_check_30day_months(self):
        for month in (4, 6, 9, 11):
            date = fd.partialdate.date.Date(None, month, 30)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, month)
            self.assertEqual(date.day, 30)

            for bad_day in (-42, -1, 0, 31, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date(
                        year=None, month=month, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..30]', message)

    def test_day_range_check_31day_months(self):
        for month in (1, 3, 5, 7, 8, 10, 12):
            date = fd.partialdate.date.Date(None, month, 31)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, month)
            self.assertEqual(date.day, 31)

            for bad_day in (-42, -1, 0, 32, 42, 10000):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date(
                        year=None, month=month, day=bad_day)
                message = str(cm.exception)
                self.assertIn('day is out of range [1..31]', message)

    def test_day_range_check_unspecified_year_month(self):
        for day in (1, 28, 29, 30, 31):
            date = fd.partialdate.date.Date(None, None, day)
            self.assertEqual(date.year, None)
            self.assertEqual(date.month, None)
            self.assertEqual(date.day, day)

        for bad_day in (-42, -1, 0, 32, 42, 10000):
            with self.assert_range_error() as cm:
                fd.partialdate.date.Date(year=None, month=None, day=bad_day)
            message = str(cm.exception)
            self.assertIn('day is out of range [1..31]', message)

    def test_rando_comparison_fully_specified(self):
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            pdate = fd.partialdate.date.Date(*ymd)
            rando = object()
            self.assertNotEqual(pdate, rando)
            with self.assertRaises(TypeError) as cm:
                pdate < rando
            message = str(cm.exception)
            self.assertIn("'<' not supported", message)
            with self.assertRaises(TypeError) as cm:
                pdate > rando
            message = str(cm.exception)
            self.assertIn("'>' not supported", message)

    def test_rando_comparison_partially_specified(self):
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(year=year, month=month)
            rando = object()
            self.assertNotEqual(pdate, rando)
            with self.assertRaises(TypeError) as cm:
                pdate < rando
            message = str(cm.exception)
            self.assertIn("'<' not supported", message)
            with self.assertRaises(TypeError) as cm:
                pdate > rando
            message = str(cm.exception)
            self.assertIn("'>' not supported", message)

    def test_datetime_comparison(self):
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29),
                    (2, 2), (2021, 11), (9998,)]:
            pdate = fd.partialdate.date.Date(*ymd)
            dt = datetime.datetime.now()

            with self.assertRaises(TypeError) as cm:
                pdate == dt
            message = str(cm.exception)
            self.assertIn('comparison not supported', message)

            with self.assertRaises(TypeError) as cm:
                pdate != dt
            message = str(cm.exception)
            self.assertIn('comparison not supported', message)

            with self.assertRaises(TypeError) as cm:
                pdate < dt
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

            with self.assertRaises(TypeError) as cm:
                pdate > dt
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

    def test_date_comparison_fully_specified(self):
        factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(*ymd)
            date = factory(*ymd)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(year-1, month, day))
            self.assertGreater(pdate, factory(year, month-1, day))
            self.assertGreater(pdate, factory(year, month, day-1))
            self.assertLess(pdate, factory(year+1, month, day))
            self.assertLess(pdate, factory(year, month+1, day))
            self.assertLess(pdate, factory(year, month, day+1))

    # Partial dates sort lower than fully specified dates, where
    # most-significant bits don't order things.
    #
    # Where most-significant bits aren't aligned, ValueError is raised.

    def test_date_comparison_y_specified(self):
        factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(year)
            date = factory(*ymd)
            self.assertNotEqual(date, pdate)
            self.assertGreater(date, pdate)
            self.assertLess(pdate, date)

    def test_date_comparison_ym_specified(self):
        factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(year, month)
            date = factory(*ymd)
            self.assertNotEqual(date, pdate)
            self.assertGreater(date, pdate)
            self.assertLess(pdate, date)

    def test_date_comparison_md_specified(self):
        factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(month=month, day=day)
            date = factory(*ymd)
            self.assertNotEqual(date, pdate)

            with self.assertRaises(ValueError) as cm:
                date < pdate
            message = str(cm.exception)
            self.assertEqual(
                message,
                'ordering not supported between incompatible partial dates')

            with self.assertRaises(ValueError) as cm:
                date > pdate
            message = str(cm.exception)
            self.assertEqual(
                message,
                'ordering not supported between incompatible partial dates')

    def test_comparison_fully_specified(self):
        factory = fd.partialdate.date.Date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = fd.partialdate.date.Date(*ymd)
            date = factory(*ymd)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(year-1, month, day))
            self.assertGreater(pdate, factory(year, month-1, day))
            self.assertGreater(pdate, factory(year, month, day-1))
            self.assertLess(pdate, factory(year+1, month, day))
            self.assertLess(pdate, factory(year, month+1, day))
            self.assertLess(pdate, factory(year, month, day+1))

    def test_comparison_partially_specified(self):
        factory = fd.partialdate.date.Date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd

            pdate = factory(year=year)
            date = factory(year=year)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(year=year-1))
            self.assertLess(pdate, factory(year=year+1))

            pdate = factory(year=year, month=month)
            date = factory(year=year, month=month)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(year-1, month))
            self.assertGreater(pdate, factory(year, month-1))
            self.assertLess(pdate, factory(year+1, month))
            self.assertLess(pdate, factory(year, month+1))

            pdate = factory(month=month, day=day)
            date = factory(month=month, day=day)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(month=month-1, day=day))
            self.assertGreater(pdate, factory(month=month, day=day-1))
            self.assertLess(pdate, factory(month=month+1, day=day))
            self.assertLess(pdate, factory(month=month, day=day+1))

            pdate = factory(day=day)
            date = factory(day=day)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(day=day-1))
            self.assertLess(pdate, factory(day=day+1))

    def test_repr_positional(self):
        date = fd.partialdate.date.Date(0)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(0)')
        date = fd.partialdate.date.Date(2012)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012)')
        date = fd.partialdate.date.Date(2012, 12)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012, 12)')
        date = fd.partialdate.date.Date(2012, 12, 8)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012, 12, 8)')

    def test_repr_keyword(self):
        date = fd.partialdate.date.Date(month=12, day=8)
        self.assertEqual(repr(date),
                         'fd.partialdate.date.Date(month=12, day=8)')
        date = fd.partialdate.date.Date(day=8)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(day=8)')

    def test_ymd_isoparse(self):
        for value in ('0000-01-01', '00000101'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 0)
            self.assertEqual(date.month, 1)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0000-01-01')
            self.assertEqual(str(date), '0000-01-01')

        for value in ('2021-12-08', '20211208'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 2021)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 8)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2021-12-08')
            self.assertEqual(str(date), '2021-12-08')

    def test_ym_isoparse(self):
        date = fd.partialdate.date.Date.isoparse('0000-01')
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000-01')
        self.assertEqual(str(date), '0000-01')

        date = fd.partialdate.date.Date.isoparse('2021-12')
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021-12')
        self.assertEqual(str(date), '2021-12')

    def test_o_isoparse(self):
        for value in ('--001', '--032', '--365', '--366', '--999',
                      '-001', '-032', '-365', '-366', '-999'):
            with self.assert_parse_error() as cm:
                fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(cm.exception.value, value)
            self.assertEqual(cm.exception.what, 'ISO 8601 date')

    def test_yo_isoparse(self):
        for value in ('0000-001', '0000001'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 0)
            self.assertEqual(date.month, 1)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0000-01-01')
            self.assertEqual(str(date), '0000-01-01')

        # Not leap year; last day of year.
        for value in ('0003-365', '0003365'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 3)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 31)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0003-12-31')
            self.assertEqual(str(date), '0003-12-31')

        # Leap year; last day of year.
        for value in ('0004-366', '0004366'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 4)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 31)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0004-12-31')
            self.assertEqual(str(date), '0004-12-31')

        # Not leap year; last day of February.
        for value in ('2000-060', '2000060'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 2000)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 29)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2000-02-29')
            self.assertEqual(str(date), '2000-02-29')

        # Not leap year; first day of March.
        for value in ('2001-060', '2001060'):
            date = fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(date.year, 2001)
            self.assertEqual(date.month, 3)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2001-03-01')
            self.assertEqual(str(date), '2001-03-01')

        for value, oday in {'0000-367': 367, '1960-999': 999}.items():
            for value in (value, value.replace('-', '')):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date.isoparse(value)
                self.assertEqual(cm.exception.field, 'ordinal day')
                self.assertEqual(cm.exception.min, 1)
                self.assertEqual(cm.exception.max, 366)
                self.assertEqual(cm.exception.value, oday)

        for value, oday in {'0001-366': 366, '1961-999': 999,
                            '9999-999': 999}.items():
            for value in (value, value.replace('-', '')):
                with self.assert_range_error() as cm:
                    fd.partialdate.date.Date.isoparse(value)
                self.assertEqual(cm.exception.field, 'ordinal day')
                self.assertEqual(cm.exception.min, 1)
                self.assertEqual(cm.exception.max, 365)
                self.assertEqual(cm.exception.value, oday)

    def test_y_isoparse(self):
        date = fd.partialdate.date.Date.isoparse('0000')
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000')
        self.assertEqual(str(date), '0000')

        date = fd.partialdate.date.Date.isoparse('2021')
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021')
        self.assertEqual(str(date), '2021')

    def test_md_isoparse(self):
        date = fd.partialdate.date.Date.isoparse('-1208')
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '-1208')
        self.assertEqual(str(date), '-1208')

    def test_d_isoparse(self):
        date = fd.partialdate.date.Date.isoparse('--08')
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '--08')
        self.assertEqual(str(date), '--08')

    def test_isoparse_failures(self):

        def check(value):
            with self.assert_parse_error() as cm:
                fd.partialdate.date.Date.isoparse(value)
            self.assertEqual(cm.exception.value, value)
            message = str(cm.exception)
            self.assertIn(repr(value), message)
            self.assertIn('text cannot be parsed', message)
            self.assertIn(cm.exception.what, message)
            self.assertEqual(cm.exception.what, 'ISO 8601 date')
            self.assertEqual(cm.exception.value, value)

        check('junky stuff')
        check('-12-')
        check('-365')
        check('--1257')
        check('2012-')
        check('2012-6')
        check('2012-6-')
        check('2012-6-10')
        check('2012-10-')
        check('2012-10-6')
        # All components are omitted.
        check('-----')
        check('---')

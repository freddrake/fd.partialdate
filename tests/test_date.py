"""\
Tests for fd.partialdate.date.

"""

import datetime
import unittest

import fd.partialdate.date
import tests.utils


class DateTestCase(
        tests.utils.AssertionHelpers,
        tests.utils.DateRangeChecks,
        unittest.TestCase):

    factory = fd.partialdate.date.Date

    def test_ymd_construction(self):
        date = self.factory(0, 12, 6)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 6)
        self.assertFalse(date.partial)
        self.assertEqual(date.isoformat(), '0000-12-06')
        self.assertEqual(date.isoformat(extended=False), '00001206')
        self.assertEqual(str(date), '0000-12-06')

        date = self.factory(2021, 12, 6)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 6)
        self.assertFalse(date.partial)
        self.assertEqual(date.isoformat(), '2021-12-06')
        self.assertEqual(date.isoformat(extended=False), '20211206')
        self.assertEqual(str(date), '2021-12-06')

    def test_ym_construction(self):
        date = self.factory(0, 12)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000-12')
        # There is only one allowed representation, and it's basic.
        self.assertEqual(date.isoformat(extended=False), '0000-12')
        self.assertEqual(str(date), '0000-12')

        date = self.factory(2021, 12)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021-12')
        self.assertEqual(date.isoformat(extended=False), '2021-12')
        self.assertEqual(str(date), '2021-12')

    def test_y_construction(self):
        date = self.factory(0)
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000')
        self.assertEqual(str(date), '0000')

        date = self.factory(2021)
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021')
        self.assertEqual(str(date), '2021')

    def test_md_construction(self):
        date = self.factory(month=12, day=8)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '-1208')
        self.assertEqual(str(date), '-1208')

    def test_d_construction(self):
        date = self.factory(day=8)
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '--08')
        self.assertEqual(str(date), '--08')

    def test_yd_construction(self):
        with self.assertRaises(ValueError) as cm:
            self.factory(0, day=6)
        self.assertEqual(str(cm.exception),
                         'cannot specify year and day without month')

        with self.assertRaises(ValueError) as cm:
            self.factory(2021, day=6)
        self.assertEqual(str(cm.exception),
                         'cannot specify year and day without month')

    def test_m_construction(self):
        with self.assertRaises(ValueError) as cm:
            self.factory(month=12)
        self.assertEqual(str(cm.exception),
                         'must specify year or day along with month')

    def test_empty_construction(self):
        with self.assertRaises(ValueError) as cm:
            self.factory()
        self.assertEqual(str(cm.exception),
                         'must specify year or day')

    def test_rando_comparison_fully_specified(self):
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            pdate = self.factory(*ymd)
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
            pdate = self.factory(year=year, month=month)
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
            pdate = self.factory(*ymd)
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
        alt_factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = self.factory(*ymd)
            date = alt_factory(*ymd)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(year-1, month, day))
            self.assertGreater(pdate, alt_factory(year, month-1, day))
            self.assertGreater(pdate, alt_factory(year, month, day-1))
            self.assertLess(pdate, alt_factory(year+1, month, day))
            self.assertLess(pdate, alt_factory(year, month+1, day))
            self.assertLess(pdate, alt_factory(year, month, day+1))

    # Partial dates sort lower than fully specified dates, where
    # most-significant bits don't order things.
    #
    # Where most-significant bits aren't aligned, ValueError is raised.

    def test_date_comparison_y_specified(self):
        alt_factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = self.factory(year)
            date = alt_factory(*ymd)
            self.assertNotEqual(date, pdate)
            self.assertGreater(date, pdate)
            self.assertLess(pdate, date)

    def test_date_comparison_ym_specified(self):
        alt_factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = self.factory(year, month)
            date = alt_factory(*ymd)
            self.assertNotEqual(date, pdate)
            self.assertGreater(date, pdate)
            self.assertLess(pdate, date)

    def test_date_comparison_md_specified(self):
        alt_factory = datetime.date
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = self.factory(month=month, day=day)
            date = alt_factory(*ymd)
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
        alt_factory = self.factory
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd
            pdate = self.factory(*ymd)
            date = alt_factory(*ymd)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(year-1, month, day))
            self.assertGreater(pdate, alt_factory(year, month-1, day))
            self.assertGreater(pdate, alt_factory(year, month, day-1))
            self.assertLess(pdate, alt_factory(year+1, month, day))
            self.assertLess(pdate, alt_factory(year, month+1, day))
            self.assertLess(pdate, alt_factory(year, month, day+1))

    def test_comparison_partially_specified(self):
        alt_factory = self.factory
        for ymd in [(2, 2, 2), (2021, 11, 8), (9998, 11, 29)]:
            year, month, day = ymd

            pdate = alt_factory(year=year)
            date = alt_factory(year=year)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(year=year-1))
            self.assertLess(pdate, alt_factory(year=year+1))

            pdate = alt_factory(year=year, month=month)
            date = alt_factory(year=year, month=month)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(year-1, month))
            self.assertGreater(pdate, alt_factory(year, month-1))
            self.assertLess(pdate, alt_factory(year+1, month))
            self.assertLess(pdate, alt_factory(year, month+1))

            pdate = alt_factory(month=month, day=day)
            date = alt_factory(month=month, day=day)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(month=month-1, day=day))
            self.assertGreater(pdate, alt_factory(month=month, day=day-1))
            self.assertLess(pdate, alt_factory(month=month+1, day=day))
            self.assertLess(pdate, alt_factory(month=month, day=day+1))

            pdate = alt_factory(day=day)
            date = alt_factory(day=day)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(day=day-1))
            self.assertLess(pdate, alt_factory(day=day+1))

    def test_repr_positional(self):
        date = self.factory(0)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(0)')
        date = self.factory(2012)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012)')
        date = self.factory(2012, 12)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012, 12)')
        date = self.factory(2012, 12, 8)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(2012, 12, 8)')

    def test_repr_keyword(self):
        date = self.factory(month=12, day=8)
        self.assertEqual(repr(date),
                         'fd.partialdate.date.Date(month=12, day=8)')
        date = self.factory(day=8)
        self.assertEqual(repr(date), 'fd.partialdate.date.Date(day=8)')

    def test_ymd_isoparse(self):
        for value in ('0000-01-01', '00000101'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 0)
            self.assertEqual(date.month, 1)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0000-01-01')
            self.assertEqual(str(date), '0000-01-01')

        for value in ('2021-12-08', '20211208'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 2021)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 8)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2021-12-08')
            self.assertEqual(str(date), '2021-12-08')

    def test_ym_isoparse(self):
        date = self.factory.isoparse('0000-01')
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000-01')
        self.assertEqual(str(date), '0000-01')

        date = self.factory.isoparse('2021-12')
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
                self.factory.isoparse(value)
            self.assertEqual(cm.exception.value, value)
            self.assertEqual(cm.exception.what, 'ISO 8601 date')

    def test_yo_isoparse(self):
        for value in ('0000-001', '0000001'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 0)
            self.assertEqual(date.month, 1)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0000-01-01')
            self.assertEqual(str(date), '0000-01-01')

        # Not leap year; last day of year.
        for value in ('0003-365', '0003365'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 3)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 31)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0003-12-31')
            self.assertEqual(str(date), '0003-12-31')

        # Leap year; last day of year.
        for value in ('0004-366', '0004366'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 4)
            self.assertEqual(date.month, 12)
            self.assertEqual(date.day, 31)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '0004-12-31')
            self.assertEqual(str(date), '0004-12-31')

        # Not leap year; last day of February.
        for value in ('2000-060', '2000060'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 2000)
            self.assertEqual(date.month, 2)
            self.assertEqual(date.day, 29)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2000-02-29')
            self.assertEqual(str(date), '2000-02-29')

        # Not leap year; first day of March.
        for value in ('2001-060', '2001060'):
            date = self.factory.isoparse(value)
            self.assertEqual(date.year, 2001)
            self.assertEqual(date.month, 3)
            self.assertEqual(date.day, 1)
            self.assertFalse(date.partial)
            self.assertEqual(date.isoformat(), '2001-03-01')
            self.assertEqual(str(date), '2001-03-01')

        for value, oday in {'0000-367': 367, '1960-999': 999}.items():
            for value in (value, value.replace('-', '')):
                with self.assert_range_error() as cm:
                    self.factory.isoparse(value)
                self.assertEqual(cm.exception.field, 'ordinal day')
                self.assertEqual(cm.exception.min, 1)
                self.assertEqual(cm.exception.max, 366)
                self.assertEqual(cm.exception.value, oday)

        for value, oday in {'0001-366': 366, '1961-999': 999,
                            '9999-999': 999}.items():
            for value in (value, value.replace('-', '')):
                with self.assert_range_error() as cm:
                    self.factory.isoparse(value)
                self.assertEqual(cm.exception.field, 'ordinal day')
                self.assertEqual(cm.exception.min, 1)
                self.assertEqual(cm.exception.max, 365)
                self.assertEqual(cm.exception.value, oday)

    def test_y_isoparse(self):
        date = self.factory.isoparse('0000')
        self.assertEqual(date.year, 0)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '0000')
        self.assertEqual(str(date), '0000')

        date = self.factory.isoparse('2021')
        self.assertEqual(date.year, 2021)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, None)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '2021')
        self.assertEqual(str(date), '2021')

    def test_md_isoparse(self):
        date = self.factory.isoparse('-1208')
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '-1208')
        self.assertEqual(str(date), '-1208')

    def test_d_isoparse(self):
        date = self.factory.isoparse('--08')
        self.assertEqual(date.year, None)
        self.assertEqual(date.month, None)
        self.assertEqual(date.day, 8)
        self.assertTrue(date.partial)
        self.assertEqual(date.isoformat(), '--08')
        self.assertEqual(str(date), '--08')

    def test_isoparse_failures(self):

        def check(value):
            with self.assert_parse_error() as cm:
                self.factory.isoparse(value)
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

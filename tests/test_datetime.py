"""\
Tests for fd.partialdate.datetime.

"""

import datetime
import unittest

import fd.partialdate.datetime
import tests.utils


class DatetimeTestCase(tests.utils.AssertionHelpers, unittest.TestCase):

    factory = fd.partialdate.datetime.Datetime

    def test_ymdhms_construction(self):
        dt = fd.partialdate.datetime.Datetime(0, 12, 6, 12, 11, 42)
        self.assertEqual(dt.year, 0)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 6)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertEqual(dt.second, 42)
        self.assertFalse(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '0000-12-06T12:11:42')
        self.assertEqual(dt.isoformat(sep=' '), '0000-12-06 12:11:42')
        self.assertEqual(dt.isoformat(extended=False), '00001206T121142')
        self.assertEqual(dt.isoformat(sep=' ', extended=False),
                         '00001206 121142')
        self.assertEqual(str(dt), '0000-12-06 12:11:42')

        dt = fd.partialdate.datetime.Datetime(2021, 12, 29, 12, 11, 42)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 29)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertEqual(dt.second, 42)
        self.assertFalse(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '2021-12-29T12:11:42')
        self.assertEqual(dt.isoformat(extended=False), '20211229T121142')
        self.assertEqual(str(dt), '2021-12-29 12:11:42')

    def test_ymdhm_construction(self):
        dt = fd.partialdate.datetime.Datetime(0, 12, 6, 12, 11)
        self.assertEqual(dt.year, 0)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 6)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertIsNone(dt.second)
        self.assertTrue(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '0000-12-06T12:11')
        self.assertEqual(dt.isoformat(sep=' '), '0000-12-06 12:11')
        self.assertEqual(dt.isoformat(extended=False), '00001206T1211')
        self.assertEqual(dt.isoformat(sep=' ', extended=False),
                         '00001206 1211')
        self.assertEqual(str(dt), '0000-12-06 12:11')

        dt = fd.partialdate.datetime.Datetime(2021, 12, 29, 12, 11)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 29)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertIsNone(dt.second)
        self.assertTrue(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '2021-12-29T12:11')
        self.assertEqual(dt.isoformat(extended=False), '20211229T1211')
        self.assertEqual(str(dt), '2021-12-29 12:11')

    def test_mdhm_construction(self):
        dt = fd.partialdate.datetime.Datetime(None, 12, 6, 12, 11)
        self.assertIsNone(dt.year)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 6)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertIsNone(dt.second)
        self.assertTrue(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '-1206T1211')
        self.assertEqual(dt.isoformat(sep=' '), '-1206 1211')
        self.assertEqual(dt.isoformat(extended=False), '-1206T1211')
        self.assertEqual(dt.isoformat(sep=' ', extended=False), '-1206 1211')
        self.assertEqual(str(dt), '-1206 1211')

        dt = fd.partialdate.datetime.Datetime(None, 12, 29, 12, 11)
        self.assertIsNone(dt.year)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 29)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 11)
        self.assertIsNone(dt.second)
        self.assertTrue(dt.partial)
        self.assertIsNone(dt.tzinfo)
        self.assertEqual(dt.isoformat(), '-1229T1211')
        self.assertEqual(dt.isoformat(extended=False), '-1229T1211')
        self.assertEqual(str(dt), '-1229 1211')

    def test_rando_comparison_fully_specified(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            ptime = fd.partialdate.datetime.Datetime(*ymdhms)
            rando = object()
            self.assertNotEqual(ptime, rando)
            with self.assertRaises(TypeError) as cm:
                ptime < rando
            message = str(cm.exception)
            self.assertIn("ordering not supported", message)
            with self.assertRaises(TypeError) as cm:
                ptime > rando
            message = str(cm.exception)
            self.assertIn("ordering not supported", message)

    def test_rando_comparison_partially_specified(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            year, month, day, hour, minute, second = ymdhms
            ptime = fd.partialdate.datetime.Datetime(
                month=month, day=day, hour=hour, minute=minute)
            rando = object()
            self.assertNotEqual(ptime, rando)
            with self.assertRaises(TypeError) as cm:
                ptime < rando
            message = str(cm.exception)
            self.assertIn("ordering not supported", message)
            with self.assertRaises(TypeError) as cm:
                ptime > rando
            message = str(cm.exception)
            self.assertIn("ordering not supported", message)

    def test_date_comparison(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            ptime = fd.partialdate.datetime.Datetime(*ymdhms)
            d = datetime.date.today()

            self.assertNotEqual(ptime, d)

    def test_date_ordering(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            ptime = fd.partialdate.datetime.Datetime(*ymdhms)
            d = datetime.date.today()

            with self.assertRaises(TypeError) as cm:
                ptime < d
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

            with self.assertRaises(TypeError) as cm:
                ptime > d
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

    def test_time_comparison(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            ptime = fd.partialdate.datetime.Datetime(*ymdhms)
            t = datetime.datetime.now().time()

            self.assertNotEqual(ptime, t)

    def test_time_ordering(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            ptime = fd.partialdate.datetime.Datetime(*ymdhms)
            t = datetime.datetime.now().time()

            with self.assertRaises(TypeError) as cm:
                ptime < t
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

            with self.assertRaises(TypeError) as cm:
                ptime > t
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

    def test_datetime_comparison_fully_specified(self):
        alt_factory = datetime.datetime
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            year, month, day, hour, minute, second = ymdhms
            pdate = fd.partialdate.datetime.Datetime(*ymdhms)
            date = alt_factory(*ymdhms)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, alt_factory(year-1, month, day,
                                                  hour, minute, second))
            self.assertGreater(pdate, alt_factory(year, month-1, day,
                                                  hour, minute, second))
            self.assertGreater(pdate, alt_factory(year, month, day-1,
                                                  hour, minute, second))
            self.assertGreater(pdate, alt_factory(year, month, day,
                                                  hour-1, minute, second))
            self.assertGreater(pdate, alt_factory(year, month, day,
                                                  hour, minute-1, second))
            self.assertGreater(pdate, alt_factory(year, month, day,
                                                  hour, minute, second-1))
            self.assertLess(pdate, alt_factory(year+1, month, day,
                                               hour, minute, second))
            self.assertLess(pdate, alt_factory(year, month+1, day,
                                               hour, minute, second))
            self.assertLess(pdate, alt_factory(year, month, day+1,
                                               hour, minute, second))
            self.assertLess(pdate, alt_factory(year, month, day,
                                               hour+1, minute, second))
            self.assertLess(pdate, alt_factory(year, month, day,
                                               hour, minute+1, second))
            self.assertLess(pdate, alt_factory(year, month, day,
                                               hour, minute, second+1))

    def test_comparison_fully_specified(self):
        factory = fd.partialdate.datetime.Datetime
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            year, month, day, hour, minute, second = ymdhms
            pdate = fd.partialdate.datetime.Datetime(*ymdhms)
            date = factory(*ymdhms)
            self.assertIsNot(pdate, date)
            self.assertEqual(pdate, date)
            self.assertGreater(pdate, factory(year-1, month, day,
                                              hour, minute, second))
            self.assertGreater(pdate, factory(year, month-1, day,
                                              hour, minute, second))
            self.assertGreater(pdate, factory(year, month, day-1,
                                              hour, minute, second))
            self.assertGreater(pdate, factory(year, month, day,
                                              hour-1, minute, second))
            self.assertGreater(pdate, factory(year, month, day,
                                              hour, minute-1, second))
            self.assertGreater(pdate, factory(year, month, day,
                                              hour, minute, second-1))
            self.assertLess(pdate, factory(year+1, month, day,
                                           hour, minute, second))
            self.assertLess(pdate, factory(year, month+1, day,
                                           hour, minute, second))
            self.assertLess(pdate, factory(year, month, day+1,
                                           hour, minute, second))
            self.assertLess(pdate, factory(year, month, day,
                                           hour+1, minute, second))
            self.assertLess(pdate, factory(year, month, day,
                                           hour, minute+1, second))
            self.assertLess(pdate, factory(year, month, day,
                                           hour, minute, second+1))

    def test_comparison_offset_aware_naive(self):
        for ymdhms in [(2, 2, 2, 2, 2, 2),
                       (2021, 11, 8, 12, 11, 42),
                       (9998, 11, 29, 22, 58, 58)]:
            lhs = fd.partialdate.datetime.Datetime(*ymdhms)
            rhs = fd.partialdate.datetime.Datetime(
                *ymdhms, tzinfo=datetime.timezone.utc)
            self.assertIsNot(lhs, rhs)
            self.assertNotEqual(lhs, rhs)
            self.assertNotEqual(rhs, lhs)

            with self.assertRaises(TypeError) as cm:
                lhs < rhs
            message = str(cm.exception)
            self.assertIn("can't order", message)
            self.assertIn('offset-naive and offset-aware', message)
            self.assertIn('time values', message)

            with self.assertRaises(TypeError) as cm:
                rhs < lhs
            message = str(cm.exception)
            self.assertIn("can't order", message)
            self.assertIn('offset-naive and offset-aware', message)
            self.assertIn('time values', message)

            with self.assertRaises(TypeError) as cm:
                lhs > rhs
            message = str(cm.exception)
            self.assertIn("can't order", message)
            self.assertIn('offset-naive and offset-aware', message)
            self.assertIn('time values', message)

    def test_comparison_complete_mixed_timezones_equal(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, 1, 15, 42, tzinfo=timezone0)
        rhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, 2, 15, 42, tzinfo=timezone1)
        assert not lhs.partial
        assert not rhs.partial

        self.assertEqual(rhs, lhs)
        self.assertEqual(lhs, rhs)

    def test_comparison_complete_mixed_timezones_unequal(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, 1, 15, 42, tzinfo=timezone0)
        rhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, 1, 15, 42, tzinfo=timezone1)
        assert not lhs.partial
        assert not rhs.partial

        self.assertGreater(lhs, rhs)
        self.assertLess(rhs, lhs)
        self.assertNotEqual(rhs, lhs)
        self.assertNotEqual(lhs, rhs)

    def test_comparison_partial_mixed_timezones(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, hour=1, tzinfo=timezone0)
        rhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29, hour=1, tzinfo=timezone1)
        assert lhs.partial
        assert rhs.partial

        with self.assertRaises(TypeError) as cm:
            lhs < rhs

        message = str(cm.exception)
        self.assertIn("can't order partial datetime values", message)
        self.assertIn('different time zones', message)

        with self.assertRaises(TypeError) as cm:
            lhs == rhs

        message = str(cm.exception)
        self.assertIn("can't compare partial datetime values", message)
        self.assertIn('different time zones', message)

    def test_comparison_mixed_partial_timezones(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29,
            hour=1, tzinfo=timezone0)
        rhs = fd.partialdate.datetime.Datetime(
            2021, 12, 29,
            hour=1, minute=15, second=42, tzinfo=timezone1)
        assert lhs.partial
        assert not rhs.partial

        with self.assertRaises(TypeError) as cm:
            lhs < rhs

        message = str(cm.exception)
        self.assertIn("can't order partial and complete datetime values",
                      message)
        self.assertIn('different time zones', message)

        with self.assertRaises(TypeError) as cm:
            lhs == rhs

        message = str(cm.exception)
        self.assertIn("can't compare partial and complete datetime values",
                      message)
        self.assertIn('different time zones', message)

    def test_repr_positional(self):
        dt = fd.partialdate.datetime.Datetime(
            year=2021, month=12, day=29, hour=12)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime(2021, 12, 29, 12)')
        dt = fd.partialdate.datetime.Datetime(
            year=2021, month=12, day=29, hour=12, minute=12)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime(2021, 12, 29, 12, 12)')
        dt = fd.partialdate.datetime.Datetime(
            year=2021, month=12, day=29, hour=12, minute=12, second=8)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime(2021, 12, 29, 12, 12, 8)')
        dt = fd.partialdate.datetime.Datetime(
            year=2021, month=12, day=29, hour=12, minute=12, second=8,
            tzinfo=datetime.timezone.utc)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime'
            '(2021, 12, 29, 12, 12, 8, datetime.timezone.utc)')

    def test_repr_keyword(self):
        dt = fd.partialdate.datetime.Datetime(month=10, day=15,
                                              minute=12, second=8)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime'
            '(month=10, day=15, minute=12, second=8)')
        dt = fd.partialdate.datetime.Datetime(day=1, second=8)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime(day=1, second=8)')
        dt = fd.partialdate.datetime.Datetime(day=1, second=8,
                                              tzinfo=datetime.timezone.utc)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime'
            '(day=1, second=8, tzinfo=datetime.timezone.utc)')

    def test_repr_mixed(self):
        dt = fd.partialdate.datetime.Datetime(year=2021, month=10, day=15,
                                              minute=12, second=8)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime'
            '(2021, 10, 15, minute=12, second=8)')
        dt = fd.partialdate.datetime.Datetime(year=2021, second=8)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime(2021, second=8)')
        dt = fd.partialdate.datetime.Datetime(year=2021, second=8,
                                              tzinfo=datetime.timezone.utc)
        self.assertEqual(
            repr(dt),
            'fd.partialdate.datetime.Datetime'
            '(2021, second=8, tzinfo=datetime.timezone.utc)')


class DateRangeCheckTestCase(
        tests.utils.AssertionHelpers,
        tests.utils.DateRangeChecks,
        unittest.TestCase):

    def factory(self, year=None, month=None, day=None):
        return fd.partialdate.datetime.Datetime(year, month, day,
                                                hour=15, minute=0, second=0)


class TimeRangeCheckTestCase(
        tests.utils.AssertionHelpers,
        tests.utils.TimeRangeChecks,
        unittest.TestCase):

    def factory(self, hour=None, minute=None, second=None, tzinfo=None):
        return fd.partialdate.datetime.Datetime(
            2021, 12, 29, hour=hour, minute=minute, second=second,
            tzinfo=tzinfo)

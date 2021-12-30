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

    def test_ymdhms_basic_isoparse(self):

        def check(dt):
            self.assertEqual(dt.year, 2021)
            self.assertEqual(dt.month, 12)
            self.assertEqual(dt.day, 30)
            self.assertEqual(dt.hour, 21)
            self.assertEqual(dt.minute, 12)
            self.assertEqual(dt.second, 8)
            self.assertFalse(dt.partial)

        for dtsep in ('t', 'T', ' '):
            naive = f'20211230{dtsep}211208'
            dt = fd.partialdate.datetime.Datetime.isoparse(naive)
            check(dt)
            self.assertEqual(dt.tzinfo, None)
            self.assertEqual(dt.isoformat(), '2021-12-30T21:12:08')
            self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12:08')
            self.assertEqual(dt.isoformat(extended=False), '20211230T211208')
            self.assertEqual(dt.isoformat(sep=' ', extended=False),
                             '20211230 211208')

            for tzpart in ('z', 'Z', '-00', '-0000', '+00', '+0000'):
                dt = fd.partialdate.datetime.Datetime.isoparse(naive + tzpart)
                check(dt)
                self.assertEqual(dt.tzinfo, datetime.timezone.utc)
                self.assertEqual(dt.isoformat(), '2021-12-30T21:12:08Z')
                self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12:08Z')
                self.assertEqual(dt.isoformat(extended=False),
                                 '20211230T211208Z')
                self.assertEqual(dt.isoformat(sep=' ', extended=False),
                                 '20211230 211208Z')

    def test_ymdhms_extended_isoparse(self):

        def check(dt):
            self.assertEqual(dt.year, 2021)
            self.assertEqual(dt.month, 12)
            self.assertEqual(dt.day, 30)
            self.assertEqual(dt.hour, 21)
            self.assertEqual(dt.minute, 12)
            self.assertEqual(dt.second, 8)
            self.assertFalse(dt.partial)

        for dtsep in ('t', 'T', ' '):
            naive = f'2021-12-30{dtsep}21:12:08'
            dt = fd.partialdate.datetime.Datetime.isoparse(naive)
            check(dt)
            self.assertEqual(dt.tzinfo, None)
            self.assertEqual(dt.isoformat(), '2021-12-30T21:12:08')
            self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12:08')
            self.assertEqual(dt.isoformat(extended=False), '20211230T211208')
            self.assertEqual(dt.isoformat(sep=' ', extended=False),
                             '20211230 211208')

            for tzpart in ('z', 'Z', '-00', '-00:00', '+00', '+00:00'):
                dt = fd.partialdate.datetime.Datetime.isoparse(naive + tzpart)
                check(dt)
                self.assertEqual(dt.tzinfo, datetime.timezone.utc)
                self.assertEqual(dt.isoformat(), '2021-12-30T21:12:08Z')
                self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12:08Z')
                self.assertEqual(dt.isoformat(extended=False),
                                 '20211230T211208Z')
                self.assertEqual(dt.isoformat(sep=' ', extended=False),
                                 '20211230 211208Z')

    def test_ymdhm_basic_isoparse(self):

        def check(dt):
            self.assertEqual(dt.year, 2021)
            self.assertEqual(dt.month, 12)
            self.assertEqual(dt.day, 30)
            self.assertEqual(dt.hour, 21)
            self.assertEqual(dt.minute, 12)
            self.assertEqual(dt.second, None)
            self.assertTrue(dt.partial)

        for dtsep in ('t', 'T', ' '):
            naive = f'20211230{dtsep}2112'
            dt = fd.partialdate.datetime.Datetime.isoparse(naive)
            check(dt)
            self.assertEqual(dt.tzinfo, None)
            self.assertEqual(dt.isoformat(), '2021-12-30T21:12')
            self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12')
            self.assertEqual(dt.isoformat(extended=False), '20211230T2112')
            self.assertEqual(dt.isoformat(sep=' ', extended=False),
                             '20211230 2112')

            for tzpart in ('z', 'Z', '-00', '-0000', '+00', '+0000'):
                dt = fd.partialdate.datetime.Datetime.isoparse(naive + tzpart)
                check(dt)
                self.assertEqual(dt.tzinfo, datetime.timezone.utc)
                self.assertEqual(dt.isoformat(), '2021-12-30T21:12Z')
                self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12Z')
                self.assertEqual(dt.isoformat(extended=False),
                                 '20211230T2112Z')
                self.assertEqual(dt.isoformat(sep=' ', extended=False),
                                 '20211230 2112Z')

    def test_ymdhm_extended_isoparse(self):

        def check(dt):
            self.assertEqual(dt.year, 2021)
            self.assertEqual(dt.month, 12)
            self.assertEqual(dt.day, 30)
            self.assertEqual(dt.hour, 21)
            self.assertEqual(dt.minute, 12)
            self.assertEqual(dt.second, None)
            self.assertTrue(dt.partial)

        for dtsep in ('t', 'T', ' '):
            naive = f'2021-12-30{dtsep}21:12'
            dt = fd.partialdate.datetime.Datetime.isoparse(naive)
            check(dt)
            self.assertEqual(dt.tzinfo, None)
            self.assertEqual(dt.isoformat(), '2021-12-30T21:12')
            self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12')
            self.assertEqual(dt.isoformat(extended=False), '20211230T2112')
            self.assertEqual(dt.isoformat(sep=' ', extended=False),
                             '20211230 2112')

            for tzpart in ('z', 'Z', '-00', '-00:00', '+00', '+00:00'):
                dt = fd.partialdate.datetime.Datetime.isoparse(naive + tzpart)
                check(dt)
                self.assertEqual(dt.tzinfo, datetime.timezone.utc)
                self.assertEqual(dt.isoformat(), '2021-12-30T21:12Z')
                self.assertEqual(dt.isoformat(sep=' '), '2021-12-30 21:12Z')
                self.assertEqual(dt.isoformat(extended=False),
                                 '20211230T2112Z')
                self.assertEqual(dt.isoformat(sep=' ', extended=False),
                                 '20211230 2112Z')

    def test_yohm_isoparse_bad_ordinal(self):
        tpart = '12:38'

        for dtsep in ('t', 'T', ' '):
            # Leap years:
            for value, oday in {'0000-367': 367, '1960-999': 999}.items():
                for value in (value, value.replace('-', '')):
                    if '-' in value:
                        value = f'{value}{dtsep}{tpart}'
                    else:
                        value = f'{value}{dtsep}{tpart.replace(":", "")}'
                    with self.assert_range_error() as cm:
                        self.factory.isoparse(value)
                    self.assertEqual(cm.exception.field, 'ordinal day')
                    self.assertEqual(cm.exception.min, 1)
                    self.assertEqual(cm.exception.max, 366)
                    self.assertEqual(cm.exception.value, oday)

            # Non-leap years:
            for value, oday in {'0001-366': 366, '1961-999': 999,
                                '9999-999': 999}.items():
                for value in (value, value.replace('-', '')):
                    if '-' in value:
                        value = f'{value}{dtsep}{tpart}'
                    else:
                        value = f'{value}{dtsep}{tpart.replace(":", "")}'
                    with self.assert_range_error() as cm:
                        self.factory.isoparse(value)
                    self.assertEqual(cm.exception.field, 'ordinal day')
                    self.assertEqual(cm.exception.min, 1)
                    self.assertEqual(cm.exception.max, 365)
                    self.assertEqual(cm.exception.value, oday)

    def test_isoparse_failures(self):

        def check(value):
            with self.assert_parse_error() as cm:
                self.factory.isoparse(value)
            self.assertEqual(cm.exception.value, value)
            message = str(cm.exception)
            self.assertIn(repr(value), message)
            self.assertIn('text cannot be parsed', message)
            self.assertIn(cm.exception.what, message)
            self.assertEqual(cm.exception.what, 'ISO 8601 datetime')
            self.assertEqual(cm.exception.value, value)

        check('junky stuff')

        # Date-like things without times:
        check('-12-')
        check('-365')
        check('--1257')
        check('2012-')
        check('2012-6')
        check('2012-6-')
        check('2012-6-10')
        check('2012-10-')
        check('2012-10-6')

        # Time-like things without dates:
        check('126')
        check('126-')
        check('12:6:-')
        check('12:25:-')
        check('12610')
        check('12:6:10')
        check('12:6:10z')
        check('12:6:10+00:30')
        check('12:46:10+0030')
        check('12106')
        check('12:10:6')
        check('-42')

        # Both components present, but still an illegal value:
        check('2021-T1337')
        check('2021-12-30T1337')
        check('20211230T13:37')

        # All components are omitted.
        check('-----T---')
        check('-----t---')
        check('----- ---')
        check('-----')
        check('---')
        check('T')
        check('t')


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

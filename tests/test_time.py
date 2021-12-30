"""\
Tests for fd.partialdate.time.

"""

import datetime
import unittest

import fd.partialdate.time
import tests.utils


class TimeTestCase(
        tests.utils.AssertionHelpers,
        tests.utils.TimeRangeChecks,
        unittest.TestCase):

    factory = fd.partialdate.time.Time

    def test_hms_construction(self):
        time = fd.partialdate.time.Time(21, 12, 6)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 6)
        self.assertEqual(time.tzinfo, None)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '21:12:06')
        self.assertEqual(time.isoformat(extended=False), '211206')

    def test_hmsz_construction(self):
        time = fd.partialdate.time.Time(21, 12, 6,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 6)
        self.assertEqual(time.tzinfo, datetime.timezone.utc)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '21:12:06Z')
        self.assertEqual(time.isoformat(extended=False), '211206Z')

    def test_hmso_construction(self):
        timezone = datetime.timezone(datetime.timedelta(hours=1))
        time = fd.partialdate.time.Time(21, 12, 6, tzinfo=timezone)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 6)
        self.assertEqual(time.tzinfo, timezone)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '21:12:06+01:00')
        self.assertEqual(time.isoformat(extended=False), '211206+0100')

    def test_hm_construction(self):
        time = fd.partialdate.time.Time(21, 12)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21:12')
        self.assertEqual(time.isoformat(extended=False), '2112')

    def test_hmz_construction(self):
        time = fd.partialdate.time.Time(21, 12,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, datetime.timezone.utc)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21:12Z')
        self.assertEqual(time.isoformat(extended=False), '2112Z')

    def test_hmo_construction(self):
        timezone = datetime.timezone(datetime.timedelta(hours=1))
        time = fd.partialdate.time.Time(21, 12, tzinfo=timezone)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, timezone)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21:12+01:00')
        self.assertEqual(time.isoformat(extended=False), '2112+0100')

    def test_h_construction(self):
        time = fd.partialdate.time.Time(21)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21')

    def test_hz_construction(self):
        time = fd.partialdate.time.Time(21,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, datetime.timezone.utc)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21Z')

    def test_ho_construction(self):
        timezone = datetime.timezone(datetime.timedelta(hours=1))
        time = fd.partialdate.time.Time(21, tzinfo=timezone)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, timezone)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21+0100')

    def test_ms_construction(self):
        time = fd.partialdate.time.Time(minute=12, second=8)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208')

    def test_msz_construction(self):
        time = fd.partialdate.time.Time(minute=12, second=8,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, datetime.timezone.utc)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208Z')

    def test_mso_construction(self):
        timezone = datetime.timezone(datetime.timedelta(hours=1))
        time = fd.partialdate.time.Time(minute=12, second=8,
                                        tzinfo=timezone)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, timezone)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208+0100')

    def test_s_construction(self):
        time = fd.partialdate.time.Time(second=8)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '--08')

    def test_sz_construction(self):
        time = fd.partialdate.time.Time(second=8,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, datetime.timezone.utc)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '--08Z')

    def test_so_construction(self):
        timezone = datetime.timezone(datetime.timedelta(hours=1))
        time = fd.partialdate.time.Time(second=8,
                                        tzinfo=timezone)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, timezone)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '--08+0100')

    def test_yd_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.time.Time(21, second=6)
        self.assertEqual(str(cm.exception),
                         'cannot specify hour and second without minute')

    def test_m_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.time.Time(minute=12)
        self.assertEqual(str(cm.exception),
                         'must specify hour or second along with minute')

    def test_empty_construction(self):
        with self.assertRaises(ValueError) as cm:
            fd.partialdate.time.Time()
        self.assertEqual(str(cm.exception),
                         'must specify hour or second')

    def test_rando_comparison_fully_specified(self):
        for hms in [(2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            ptime = fd.partialdate.time.Time(*hms)
            rando = object()
            self.assertNotEqual(ptime, rando)
            with self.assertRaises(TypeError) as cm:
                ptime < rando
            message = str(cm.exception)
            self.assertIn("'<' not supported", message)
            with self.assertRaises(TypeError) as cm:
                ptime > rando
            message = str(cm.exception)
            self.assertIn("'>' not supported", message)

    def test_rando_comparison_partially_specified(self):
        for hms in [(2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(hour=hour, minute=minute)
            rando = object()
            self.assertNotEqual(ptime, rando)
            with self.assertRaises(TypeError) as cm:
                ptime < rando
            message = str(cm.exception)
            self.assertIn("'<' not supported", message)
            with self.assertRaises(TypeError) as cm:
                ptime > rando
            message = str(cm.exception)
            self.assertIn("'>' not supported", message)

    def test_datetime_comparison(self):
        for hms in [(2, 2, 2), (21, 11, 8), (23, 59, 59),
                    (2, 2), (21, 11), (23,)]:
            ptime = fd.partialdate.time.Time(*hms)
            dt = datetime.datetime.now()

            with self.assertRaises(TypeError) as cm:
                ptime == dt
            message = str(cm.exception)
            self.assertIn('comparison not supported', message)

            with self.assertRaises(TypeError) as cm:
                ptime != dt
            message = str(cm.exception)
            self.assertIn('comparison not supported', message)

            with self.assertRaises(TypeError) as cm:
                ptime < dt
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

            with self.assertRaises(TypeError) as cm:
                ptime > dt
            message = str(cm.exception)
            self.assertIn('ordering not supported', message)

    def test_time_comparison_fully_specified(self):
        alt_factory = datetime.time
        for hms in [(2, 2, 2), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(*hms)
            time = alt_factory(*hms)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, alt_factory(hour-1, minute, second))
            self.assertGreater(ptime, alt_factory(hour, minute-1, second))
            self.assertGreater(ptime, alt_factory(hour, minute, second-1))
            self.assertLess(ptime, alt_factory(hour+1, minute, second))
            self.assertLess(ptime, alt_factory(hour, minute+1, second))
            self.assertLess(ptime, alt_factory(hour, minute, second+1))

    # Partial times sort lower than fully specified times, where
    # most-significant bits don't order things.
    #
    # Where most-significant bits aren't aligned, ValueError is raised.

    def test_time_comparison_h_specified(self):
        alt_factory = datetime.time
        for hms in [(0, 0, 0), (2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(hour)
            time = alt_factory(*hms)
            self.assertNotEqual(time, ptime)
            self.assertGreater(time, ptime)
            self.assertLess(ptime, time)

    def test_time_comparison_hm_specified(self):
        alt_factory = datetime.time
        for hms in [(0, 0, 0), (2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(hour, minute)
            time = alt_factory(*hms)
            self.assertNotEqual(time, ptime)
            self.assertGreater(time, ptime)
            self.assertLess(ptime, time)

    def test_time_comparison_ms_specified(self):
        alt_factory = datetime.time
        for hms in [(0, 0, 0), (2, 2, 2), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(minute=minute, second=second)
            time = alt_factory(*hms)
            self.assertNotEqual(time, ptime)

            with self.assertRaises(ValueError) as cm:
                time < ptime
            message = str(cm.exception)
            self.assertEqual(
                message,
                'ordering not supported between incompatible partial times')

            with self.assertRaises(ValueError) as cm:
                time > ptime
            message = str(cm.exception)
            self.assertEqual(
                message,
                'ordering not supported between incompatible partial times')

    def test_comparison_fully_specified(self):
        alt_factory = fd.partialdate.time.Time
        for hms in [(1, 1, 1), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(*hms)
            time = alt_factory(*hms)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, alt_factory(hour-1, minute, second))
            self.assertGreater(ptime, alt_factory(hour, minute-1, second))
            self.assertGreater(ptime, alt_factory(hour, minute, second-1))
            self.assertLess(ptime, alt_factory(hour+1, minute, second))
            self.assertLess(ptime, alt_factory(hour, minute+1, second))
            self.assertLess(ptime, alt_factory(hour, minute, second+1))

    def test_comparison_offset_aware_naive(self):
        for hms in [(1, 1, 1), (21, 11, 8), (22, 58, 58)]:
            lhs = self.factory(*hms)
            rhs = self.factory(*hms, tzinfo=datetime.timezone.utc)
            self.assertIsNot(lhs, rhs)
            self.assertNotEqual(lhs, rhs)

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

    def test_comparison_partially_specified(self):
        factory = fd.partialdate.time.Time
        for hms in [(1, 1, 1), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms

            ptime = factory(hour=hour)
            time = factory(hour=hour)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(hour=hour-1))
            self.assertLess(ptime, factory(hour=hour+1))

            ptime = factory(hour=hour, minute=minute)
            time = factory(hour=hour, minute=minute)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(hour-1, minute))
            self.assertGreater(ptime, factory(hour, minute-1))
            self.assertLess(ptime, factory(hour+1, minute))
            self.assertLess(ptime, factory(hour, minute+1))

            ptime = factory(minute=minute, second=second)
            time = factory(minute=minute, second=second)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(minute=minute-1, second=second))
            self.assertGreater(ptime, factory(minute=minute, second=second-1))
            self.assertLess(ptime, factory(minute=minute+1, second=second))
            self.assertLess(ptime, factory(minute=minute, second=second+1))

            # Comparisons of partial times work with the same timezone:
            ptime = factory(minute=minute, second=second,
                            tzinfo=datetime.timezone.utc)
            time = factory(minute=minute, second=second,
                           tzinfo=datetime.timezone.utc)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(minute=minute-1, second=second,
                                              tzinfo=datetime.timezone.utc))
            self.assertGreater(ptime, factory(minute=minute, second=second-1,
                                              tzinfo=datetime.timezone.utc))
            self.assertLess(ptime, factory(minute=minute+1, second=second,
                                           tzinfo=datetime.timezone.utc))
            self.assertLess(ptime, factory(minute=minute, second=second+1,
                                           tzinfo=datetime.timezone.utc))

            ptime = factory(second=second)
            time = factory(second=second)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(second=second-1))
            self.assertLess(ptime, factory(second=second+1))

    def test_comparison_complete_mixed_timezones_equal(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = self.factory(hour=1, minute=15, second=42, tzinfo=timezone0)
        rhs = self.factory(hour=2, minute=15, second=42, tzinfo=timezone1)
        assert not lhs.partial
        assert not rhs.partial

        self.assertEqual(rhs, lhs)
        self.assertEqual(lhs, rhs)

    def test_comparison_complete_mixed_timezones_unequal(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = self.factory(hour=1, minute=15, second=42, tzinfo=timezone0)
        rhs = self.factory(hour=1, minute=15, second=42, tzinfo=timezone1)
        assert not lhs.partial
        assert not rhs.partial

        self.assertGreater(lhs, rhs)
        self.assertLess(rhs, lhs)
        self.assertNotEqual(rhs, lhs)
        self.assertNotEqual(lhs, rhs)

    def test_comparison_partial_mixed_timezones(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = self.factory(hour=1, tzinfo=timezone0)
        rhs = self.factory(hour=1, tzinfo=timezone1)
        assert lhs.partial
        assert rhs.partial

        with self.assertRaises(TypeError) as cm:
            lhs < rhs

        message = str(cm.exception)
        self.assertIn("can't order partial time values", message)
        self.assertIn('different time zones', message)

        with self.assertRaises(TypeError) as cm:
            lhs == rhs

        message = str(cm.exception)
        self.assertIn("can't compare partial time values", message)
        self.assertIn('different time zones', message)

    def test_comparison_mixed_partial_timezones(self):
        timezone0 = datetime.timezone.utc
        timezone1 = datetime.timezone(datetime.timedelta(hours=1))

        lhs = self.factory(hour=1, tzinfo=timezone0)
        rhs = self.factory(hour=1, minute=15, second=42, tzinfo=timezone1)
        assert lhs.partial
        assert not rhs.partial

        with self.assertRaises(TypeError) as cm:
            lhs < rhs

        message = str(cm.exception)
        self.assertIn("can't order partial and complete time values", message)
        self.assertIn('different time zones', message)

        with self.assertRaises(TypeError) as cm:
            lhs == rhs

        message = str(cm.exception)
        self.assertIn("can't compare partial and complete time values",
                      message)
        self.assertIn('different time zones', message)

    def test_repr_positional(self):
        time = fd.partialdate.time.Time(12)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12)')
        time = fd.partialdate.time.Time(12, 12)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12, 12)')
        time = fd.partialdate.time.Time(12, 12, 8)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12, 12, 8)')
        time = fd.partialdate.time.Time(12, 12, 8,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(
            repr(time),
            'fd.partialdate.time.Time(12, 12, 8, datetime.timezone.utc)')

    def test_repr_keyword(self):
        time = fd.partialdate.time.Time(minute=12, second=8)
        self.assertEqual(repr(time),
                         'fd.partialdate.time.Time(minute=12, second=8)')
        time = fd.partialdate.time.Time(second=8)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(second=8)')
        time = fd.partialdate.time.Time(second=8,
                                        tzinfo=datetime.timezone.utc)
        self.assertEqual(
            repr(time),
            'fd.partialdate.time.Time(second=8, tzinfo=datetime.timezone.utc)')

    def test_hms_basic_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('211208')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '21:12:08')
        self.assertEqual(time.isoformat(extended=False), '211208')

        for tzpart in ('z', 'Z', '-00', '+00', '-0000', '+0000'):
            time = fd.partialdate.time.Time.isoparse('211208' + tzpart)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, 12)
            self.assertEqual(time.second, 8)
            self.assertEqual(time.tzinfo, datetime.timezone.utc)
            self.assertFalse(time.partial)
            self.assertEqual(time.isoformat(), '21:12:08Z')
            self.assertEqual(time.isoformat(extended=False), '211208Z')

    def test_hms_extended_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('21:12:08')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '21:12:08')
        self.assertEqual(time.isoformat(extended=False), '211208')

        for tzpart in ('z', 'Z', '-00', '-00:00', '+00', '+00:00'):
            time = fd.partialdate.time.Time.isoparse('21:12:08' + tzpart)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, 12)
            self.assertEqual(time.second, 8)
            self.assertEqual(time.tzinfo, datetime.timezone.utc)
            self.assertFalse(time.partial)
            self.assertEqual(time.isoformat(), '21:12:08Z')
            self.assertEqual(time.isoformat(extended=False), '211208Z')

    def test_hm_basic_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('2112')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21:12')
        self.assertEqual(time.isoformat(extended=False), '2112')

        for tzpart in ('z', 'Z', '+00', '+0000'):
            time = fd.partialdate.time.Time.isoparse('2112' + tzpart)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, 12)
            self.assertEqual(time.second, None)
            self.assertEqual(time.tzinfo, datetime.timezone.utc)
            self.assertTrue(time.partial)
            self.assertEqual(time.isoformat(), '21:12Z')
            self.assertEqual(time.isoformat(extended=False), '2112Z')

    def test_hm_extended_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('21:12')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21:12')
        self.assertEqual(time.isoformat(extended=False), '2112')

        for tzpart in ('z', 'Z', '+00', '+00:00'):
            time = fd.partialdate.time.Time.isoparse('21:12' + tzpart)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, 12)
            self.assertEqual(time.second, None)
            self.assertEqual(time.tzinfo, datetime.timezone.utc)
            self.assertTrue(time.partial)
            self.assertEqual(time.isoformat(), '21:12Z')
            self.assertEqual(time.isoformat(extended=False), '2112Z')

    def test_h_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('21')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, None)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21')

    def test_ms_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('-1208')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208')

        time = fd.partialdate.time.Time.isoparse('-1208+01')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(
            time.tzinfo,
            datetime.timezone(datetime.timedelta(seconds=3600)))
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208+0100')

        time = fd.partialdate.time.Time.isoparse('-1208+0130')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(
            time.tzinfo,
            datetime.timezone(datetime.timedelta(seconds=5400)))
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208+0130')

        time = fd.partialdate.time.Time.isoparse('-1208-03')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(
            time.tzinfo,
            datetime.timezone(datetime.timedelta(days=-1, seconds=75600)))
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208-0300')

        time = fd.partialdate.time.Time.isoparse('-1208-0310')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertEqual(
            time.tzinfo,
            datetime.timezone(datetime.timedelta(days=-1, seconds=75000)))
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208-0310')

    def test_s_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('--08')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
        self.assertEqual(time.tzinfo, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '--08')

    def test_isoparse_failures(self):

        def check(value):
            with self.assert_parse_error() as cm:
                fd.partialdate.time.Time.isoparse(value)
            self.assertEqual(cm.exception.value, value)
            message = str(cm.exception)
            self.assertIn(repr(value), message)
            self.assertIn('text cannot be parsed', message)
            self.assertIn(cm.exception.what, message)
            self.assertEqual(cm.exception.what, 'ISO 8601 time')
            self.assertEqual(cm.exception.value, value)

        check('junky stuff')
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
        # All components are omitted.
        check('---')

"""\
Tests for fd.partialdate.time.

"""

import datetime
import unittest

import fd.partialdate.time
import tests.utils


class TimeTestCase(tests.utils.AssertionHelpers, unittest.TestCase):

    def test_hms_construction(self):
        time = fd.partialdate.time.Time(21, 12, 6)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 6)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '211206')

    def test_hm_construction(self):
        time = fd.partialdate.time.Time(21, 12)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '2112')

    def test_y_construction(self):
        time = fd.partialdate.time.Time(21)
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, None)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '21')

    def test_ms_construction(self):
        time = fd.partialdate.time.Time(minute=12, second=8)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208')

    def test_d_construction(self):
        time = fd.partialdate.time.Time(second=8)
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '--08')

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
        factory = datetime.time
        for hms in [(2, 2, 2), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(*hms)
            time = factory(*hms)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(hour-1, minute, second))
            self.assertGreater(ptime, factory(hour, minute-1, second))
            self.assertGreater(ptime, factory(hour, minute, second-1))
            self.assertLess(ptime, factory(hour+1, minute, second))
            self.assertLess(ptime, factory(hour, minute+1, second))
            self.assertLess(ptime, factory(hour, minute, second+1))

    # Partial times sort lower than fully specified times, where
    # most-significant bits don't order things.
    #
    # Where most-significant bits aren't aligned, ValueError is raised.

    def test_time_comparison_y_specified(self):
        factory = datetime.time
        for hms in [(2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(hour)
            time = factory(*hms)
            self.assertNotEqual(time, ptime)
            self.assertGreater(time, ptime)
            self.assertLess(ptime, time)

    def test_time_comparison_hm_specified(self):
        factory = datetime.time
        for hms in [(2, 2, 2), (21, 11, 8), (23, 59, 59)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(hour, minute)
            time = factory(*hms)
            self.assertNotEqual(time, ptime)
            self.assertGreater(time, ptime)
            self.assertLess(ptime, time)

    def test_time_comparison_ms_specified(self):
        factory = datetime.time
        for hms in [(2, 2, 2), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(minute=minute, second=second)
            time = factory(*hms)
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
        factory = fd.partialdate.time.Time
        for hms in [(2, 2, 2), (21, 11, 8), (22, 58, 58)]:
            hour, minute, second = hms
            ptime = fd.partialdate.time.Time(*hms)
            time = factory(*hms)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(hour-1, minute, second))
            self.assertGreater(ptime, factory(hour, minute-1, second))
            self.assertGreater(ptime, factory(hour, minute, second-1))
            self.assertLess(ptime, factory(hour+1, minute, second))
            self.assertLess(ptime, factory(hour, minute+1, second))
            self.assertLess(ptime, factory(hour, minute, second+1))

    def test_comparison_partially_specified(self):
        factory = fd.partialdate.time.Time
        for hms in [(2, 2, 2), (21, 11, 8), (22, 58, 58)]:
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

            ptime = factory(second=second)
            time = factory(second=second)
            self.assertIsNot(ptime, time)
            self.assertEqual(ptime, time)
            self.assertGreater(ptime, factory(second=second-1))
            self.assertLess(ptime, factory(second=second+1))

    def test_repr_positional(self):
        time = fd.partialdate.time.Time(12)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12)')
        time = fd.partialdate.time.Time(12, 12)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12, 12)')
        time = fd.partialdate.time.Time(12, 12, 8)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(12, 12, 8)')

    def test_repr_keyword(self):
        time = fd.partialdate.time.Time(minute=12, second=8)
        self.assertEqual(repr(time),
                         'fd.partialdate.time.Time(minute=12, second=8)')
        time = fd.partialdate.time.Time(second=8)
        self.assertEqual(repr(time), 'fd.partialdate.time.Time(second=8)')

    def test_hms_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('211208')
        self.assertEqual(time.hour, 21)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertFalse(time.partial)
        self.assertEqual(time.isoformat(), '211208')

    def test_hm_isoparse(self):
        for value in ('2112', '2112-'):
            time = fd.partialdate.time.Time.isoparse(value)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, 12)
            self.assertEqual(time.second, None)
            self.assertTrue(time.partial)
            self.assertEqual(time.isoformat(), '2112')

    def test_h_isoparse(self):
        for value in ('21', '21-', '21--'):
            time = fd.partialdate.time.Time.isoparse(value)
            self.assertEqual(time.hour, 21)
            self.assertEqual(time.minute, None)
            self.assertEqual(time.second, None)
            self.assertTrue(time.partial)
            self.assertEqual(time.isoformat(), '21')

    def test_ms_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('-1208')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, 12)
        self.assertEqual(time.second, 8)
        self.assertTrue(time.partial)
        self.assertEqual(time.isoformat(), '-1208')

    def test_s_isoparse(self):
        time = fd.partialdate.time.Time.isoparse('--08')
        self.assertEqual(time.hour, None)
        self.assertEqual(time.minute, None)
        self.assertEqual(time.second, 8)
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
        check('12610')
        check('12106')
        # All components are omitted.
        check('---')
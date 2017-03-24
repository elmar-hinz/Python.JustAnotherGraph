from types import SimpleNamespace

from jag.signalslot import SignalSlot
from unittest import TestCase


class SignalSlotTest(TestCase):
    def setUp(self):
        self.object = SignalSlot()

    def test_slots(self):
        def method1(): pass

        def method2(): pass

        self.object.slot('signal1', method1)
        self.object.slot('signal1', method2)
        self.object.slot('signal2', method1)
        signal1 = self.object._slots['signal1']
        signal2 = self.object._slots['signal2']
        self.assertEqual([method1, method2], signal1)
        self.assertEqual([method1], signal2)

    def test_signal_simple_method(self):
        ns = SimpleNamespace()
        ns.c1 = 0

        def method1():
            ns.c1 += 1

        self.object.slot('signal1', method1)
        self.object.signal('signal1')
        self.object.signal('signal1')
        self.assertEqual(2, ns.c1)

    def test_signal_method_with_diverse_arguments(self):
        def method1(a, b, *args, **kwargs):
            self.assertEqual(a, 1)
            self.assertEqual(b, 2)
            self.assertEqual(args, (3, 4))
            self.assertEqual(kwargs, {'c': 5, 'd': 6})

        self.object.slot('signal1', method1)
        self.object.signal('signal1', 1, 2, 3, 4, c=5, d=6)

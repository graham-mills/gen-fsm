from tests.end_to_end import EndToEndTestCase
from pathlib import Path
from unittest.mock import Mock, call


class T1_pass_through(EndToEndTestCase):
    def test_T1_pass_through(self):
        self.setup_test("T1_pass_through")
        self.run_test()


class T2_composite_pass_through(EndToEndTestCase):
    def test_T2_composite_pass_through(self):
        self.setup_test("T2_composite_pass_through")
        self.run_test()


class T3_nested_entry_exit(EndToEndTestCase):
    def test_T3_nested_entry_exit(self):
        self.setup_test("T3_nested_entry_exit")
        self.run_test()


class T4_cross_region_entry_exit(EndToEndTestCase):
    def test_T4_cross_region_entry_exit(self):
        self.setup_test("T4_cross_region_entry_exit")
        self.run_test()


class T5_event_pass_through(EndToEndTestCase):
    def test_T5_event_pass_through(self):
        self.setup_test("T5_event_pass_through")
        self.run_test()


class T6_event_actions(EndToEndTestCase):
    def test_T6_event_actions(self):
        self.setup_test("T6_event_actions")
        self.run_test()

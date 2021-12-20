from pathlib import Path
import gen_fsm.main
import shutil
import importlib
import sys
import logging
from unittest.mock import Mock, call
from tests.utilities import TestCaseBase
from typing import List


class EndToEndTestCase(TestCaseBase):
    def setup_test(self, test_name: str):
        # Remove and re-create test output dir
        self.output_dir = Path(__file__).parent.absolute() / "results" / test_name
        shutil.rmtree(self.output_dir, ignore_errors=True)
        self.output_dir.mkdir(parents=True)

        # Setup log file in output dir
        self.log_file = self.output_dir / "test.log"
        logging.basicConfig(filename=self.log_file, filemode="w", level=logging.DEBUG)

        # Override program args for gen_fsm to use
        self.input_file = (
            Path(__file__).parent.absolute() / "diagrams" / (test_name + ".puml")
        )
        sys.argv = [__name__, str(self.input_file), str(self.output_dir), "--diag"]

    def run_program(self):
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        program = gen_fsm.main.Program(enable_stdout_debug=lambda: None)
        program.run()

    def load_expected_actions(self) -> List[str]:
        expected_actions: List[str] = []
        line = ""
        start_tag_found = False
        with open(self.input_file, mode="r") as file:
            while line := file.readline():
                if not start_tag_found:
                    start_tag_found = line.startswith("@startexpected")
                elif line.startswith("@endexpected"):
                    break
                else:
                    expected_actions.append(call(line.strip()))

        if not start_tag_found:
            raise RuntimeError(f"{self.input_file}\n @startexpected section not found")

        if not expected_actions:
            raise RuntimeError(f"{self.input_file}\n @startexpected section empty")

        return expected_actions

    def import_statemachine_module(self):
        sys.path.append(str(self.output_dir))
        spec = importlib.util.spec_from_file_location(
            "statemachine", self.output_dir / "statemachine.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def run_test(self):
        self.run_program()

        module = self.import_statemachine_module()
        sm = module.Statemachine()
        sm.action = Mock()
        sm.start()

        expected_action_calls = self.load_expected_actions()
        sm.action.assert_has_calls(expected_action_calls, any_order=False)

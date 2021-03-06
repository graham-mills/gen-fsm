from pathlib import Path
import gen_fsm.main
import shutil
import importlib
import sys
import logging
from unittest.mock import Mock
from tests.utilities import TestCaseBase


class EndToEndTestCase(TestCaseBase):
    def setUp(self, test_name: str):
        super().setUp()
        self.test_name = test_name

        self.output_dir = Path(__file__).parent.absolute() / "output" / test_name
        shutil.rmtree(self.output_dir, ignore_errors=True)
        self.output_dir.mkdir(parents=True)

        self.log_file = self.output_dir / "test.log"
        logging.basicConfig(filename=self.log_file, filemode="w", level=logging.DEBUG)

        self.input_file = (
            Path(__file__).parent.absolute() / "diagrams" / (test_name + ".puml")
        )
        sys.argv = [__name__, str(self.input_file), str(self.output_dir), "--diag"]
        # Add the output dir to the path to import the generated modules from
        sys.path.append(str(self.output_dir))

    def run_program(self):
        logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
        program = gen_fsm.main.Program(enable_stdout_debug=lambda: None)
        program.run()

    def import_statemachine_module(self):
        spec = importlib.util.spec_from_file_location(
            "statemachine", self.output_dir / "statemachine.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

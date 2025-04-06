import subprocess
import os
from ..tester import Tester
from ..specs import TestSpecs


class ContainerTester(Tester):
    def __init__(self, specs: TestSpecs) -> None:
        """Initialize a ContainerTester"""
        super().__init__(specs, test_class=None)

    @Tester.run_decorator
    def run(self) -> None:
        """
        Run a containerized test and print the results to stdout
        - because users must be able to upload a new sif file for testing, on run, we need to check if the container has been built.
        - unfortunately, I don't think the building for instructor uploaded containers can be done on setup because setup happens at standup time, not runtime
        - The default image can be built at setup though and is
        - #TODO: add ubuntu24.def to a file which lists defaults so this isn't hardcoded and can be easily updated
        """
        image_def_file = self.specs["env_data", "image_definition_file_name"]
        image_file = os.path.splitext(image_def_file)[0] + ".sif"

        if image_def_file != "ubuntu24.def" or not os.path.exists(image_file):
            subprocess.run(["apptainer", "build", image_file, image_def_file])

        file_paths = self.specs["test_data", "script_files"]
        for file_path in file_paths:
            subprocess.run(["apptainer", "exec", f"./{image_file}", f"./{file_path}"])

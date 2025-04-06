import os
import shutil
from conan import ConanFile
from conan.tools.build import cross_building
from conan.tools.env import VirtualBuildEnv, VirtualRunEnv


class TestPackageConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"

    @property
    def file_io(self):
        return {
            "c": {
                "compiler": "arm-none-eabi-gcc",
            },
            "cpp": {
                "compiler": "arm-none-eabi-g++",
            }

        }

    def requirements(self):
        self.requires(self.tested_reference_str)

    def generate(self):
        buildenv = VirtualBuildEnv(self)
        buildenv.generate()

        runenv = VirtualRunEnv(self)
        runenv.generate()

    def build(self):
        for language, files in self.file_io.items():
            self.output.info(f"Testing build using {language} compiler")
            # Confirm compiler is propagated to env
            self.run(f"{files['compiler']} --version", env="conanrun")
            self.run(f"{files['compiler']} -dumpversion", env="conanrun")

    def test(self):
        pass

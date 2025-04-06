import os

from conan import ConanFile
from conan.tools.files import get, copy


required_conan_version = ">=2.0.0"


class GCCArmNoneEabiConan(ConanFile):
    name = "gcc-arm-none-eabi"
    package_type = "application"
    description = "Arm GNU Toolchain is a community supported pre-built GNU compiler toolchain for Arm based CPUs."
    topics = ("build", "compiler")
    url = "https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads"
    homepage = "https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads"
    license = "GPL"
    settings = "os", "arch"
    package_type = "application"

    def build(self):
        arch = str(
            self.settings.arch) if self.settings.os != "Macos" else "universal"
        
        strip_root = self.conan_data["sources"][self.version][str(self.settings.os)][arch]["url"].endswith("tar.xz")
        
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][arch],
            destination=self.source_folder, strip_root=strip_root)

    def package_id(self):
        if self.info.settings.os == "Macos":
            del self.info.settings.arch

    def package(self):
        copy(self, "*", src=self.source_folder, dst=self.package_folder)

    def package_info(self):
        self.buildenv_info.define("ARMGCC_DIR", self.package_folder)
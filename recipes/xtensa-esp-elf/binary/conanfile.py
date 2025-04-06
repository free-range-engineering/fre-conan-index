import os

from conan import ConanFile
from conan.tools.files import get, copy


required_conan_version = ">=2.0.0"


class GCCArmNoneEabiConan(ConanFile):
    name = "xtensa-esp-elf"
    package_type = "application"
    description = "Precompiled GCC toolchain for Xtensa processors used in ESP32 and similar chips."
    topics = ("compiler", "esp32", "xtensa", "toolchain", "gcc")
    url = "https://github.com/espressif/crosstool-NG"
    homepage = "https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/linux-setup.html#toolchain-setup"
    license = "GPL-2.0-or-later"
    settings = "os", "arch"

    def build(self):
        arch = str(
            self.settings.arch) if self.settings.os != "Macos" else "universal"
        
        get(self, **self.conan_data["sources"][self.version][str(self.settings.os)][arch],
            destination=self.source_folder, strip_root=True)

    def package_id(self):
        if self.info.settings.os == "Macos":
            del self.info.settings.arch

    def package(self):
        copy(self, "*", src=self.source_folder, dst=self.package_folder)

    def package_info(self):
        self.buildenv_info.define("XTENSAGCC_DIR", self.package_folder)
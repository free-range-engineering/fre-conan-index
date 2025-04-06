from invoke import task
from dataclasses import dataclass
import yaml
import os
import platform
import shutil
from enum import Enum
import subprocess

root_folder = os.path.dirname(os.path.abspath(__file__))
build_folder = os.path.join(root_folder, "build")
profile_folder = os.path.join(root_folder, "config", "profiles")


@dataclass
class Package:
    name: str
    version: str
    host_profiles: list[str]
    build_profiles: list[str] = None


build_profiles = {"64bit": {"windows": "x64_windows", "linux": "x64_linux"}}

packages = [Package("gcc-arm-none-eabi", "14.2", None,
                    ["arm6_gcc_baremetal", "libstdc++11"]),Package("xtensa-esp-elf", "14.2.0", None,
                    ["xtensalx7_gcc_baremetal", "libstdc++11"])]



class Output:
    _BOLD = "\033[1m"
    _RESET = "\033[0m"
    _COLOR_INFO = "\033[0;32m"      # Green
    _COLOR_WARN = "\033[0;33m"      # Yellow
    _COLOR_ERROR = "\033[0;31m"     # Red
    _COLOR_CRITICAL = "\033[1;31m"  # Bright Red
    _COLOR_DEBUG = "\033[0;36m"     # Cyan
    _COLOR_TRACE = "\033[2;37m"     # White
    _COLOR_HEADING = "\033[0;36m"   # Purple

    def info(self, message: str):
        print(f"{self._COLOR_INFO}INFO: {message}{self._RESET}")

    def warn(self, message: str):
        print(f"{self._COLOR_WARN}WARN: {message}{self._RESET}")

    def error(self, message: str):
        print(f"{self._COLOR_ERROR}ERROR: {message}{self._RESET}")

    def critical(self, message: str):
        print(f"{self._COLOR_CRITICAL}CRITICAL: {message}{self._RESET}")

    def debug(self, message: str):
        print(f"{self._COLOR_DEBUG}DEBUG: {message}{self._RESET}")

    def trace(self, message: str):
        print(f"{self._COLOR_TRACE}TRACE: {message}{self._RESET}")

    def heading(self, title: str):
        print(
            f"{self._BOLD}{self._COLOR_HEADING}{'=' * 8} {title} {'=' * 8}{self._RESET}")


output = Output()


def get_recipe_path(package):
    package_config_file_path = os.path.join(
        root_folder, "recipes", package.name, "config.yml")
    if os.path.exists(package_config_file_path):
        with open(package_config_file_path, "r") as file:
            if folder := yaml.safe_load(file).get("versions", {}).get(package.version, {}):
                return os.path.join(root_folder, "recipes", package.name, folder["folder"])
    else:
        output.error(f"File {package_config_file_path} does not exist")

    return None


def _conan_create(c, build_profile, filter="*"):
    for package in packages:
        if filter != "*" and filter not in package.name:
            output.trace(
                f"Package '{package.name}' filterd out by '{filter}' ")
            continue

        output.heading(f"Createing package '{package}'")

        package_build_folder = os.path.join(build_folder, package.name)
        output.trace(f"Created {package_build_folder}")
        os.makedirs(package_build_folder, exist_ok=True)
        with c.cd(package_build_folder):

            expanded_build_profile = [
                f'--profile:build="{os.path.join(profile_folder, profile)}"' for profile in package.build_profiles + [build_profile]]

            if package.host_profiles:
                expanded_host_profile = [
                    f'--profile:host="{os.path.join(profile_folder, profile)}"' for profile in package.host_profiles]
            else:
                expanded_host_profile = [
                    f'--profile:host="{os.path.join(profile_folder, profile)}"' for profile in package.build_profiles + [build_profile]]

            output.info(f"Host profiles '{expanded_host_profile}'")
            output.info(f"Build profile '{expanded_build_profile}'")
            if recipe_path := get_recipe_path(package):
                cmd = " ".join([
                    "conan",
                    "create",
                    f'--version={package.version}',
                    f'"{recipe_path}"',

                ]+expanded_host_profile+expanded_build_profile)
                output.trace(cmd)
                # inv does not like "" in the command
                try:
                    subprocess.run(cmd, check=True, shell=True)
                    output.info(f"Created package '{package}'")
                except subprocess.CalledProcessError as e:
                    output.error(
                        f"Command failed with return code {e.returncode}: {e}")
            else:
                output.error(f"Unable to find recipe_path for {package}")


@task()
def clean(c):
    """
    Cleans the build tree
    """
    if os.path.exists(build_folder):
        output.trace(f"Removed {build_folder}")
        shutil.rmtree(build_folder)
    os.makedirs(build_folder, exist_ok=True)


@task(clean)
def create(c, filter="*"):
    """
    Create Conan packages for the current system architecture and OS of the defined packages
    """
    arch = platform.architecture()[0].lower()
    os_name = platform.system().lower()

    if profile := (build_profiles.get(arch, {}).get(os_name, {})):
        profile_path = os.path.join(profile_folder, profile)
        if os.path.exists(os.path.join(profile_folder, profile)):
            output.heading(
                f"Creating packages for {arch}, {os_name} using profile --profile:build='{profile}'")
            _conan_create(c, profile, filter)
        else:
            output.error(f"Profile {profile_path} does not exist")
    else:
        output.error(f"Unsupported build enviroment {arch}, {os_name}")


@task()
def release(c, dry_run=True):
    """
    Release/Bump the version using commitizen (cz).

    Parameters:
    dry_run (bool): If True, perform a dry run without making any changes. Default is True.
    """
    c.run(f"cz bump {'--dry-run' if dry_run else ''}")

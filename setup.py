import atexit
import os.path
import platform
from setuptools import setup
import shutil
import tarfile
import tempfile
import urllib.request

setupDir = os.path.dirname(__file__)
with open(os.path.join(setupDir, ".version.actionlint")) as vH:
    actionlint_version = vH.read().strip()

with open(os.path.join(setupDir, ".version.shellcheck")) as vH:
    shellcheck_version = vH.read().strip()

machine = platform.machine()
if machine == "x86_64":
    go_machine = "amd64"
elif machine == "aarch64":
    go_machine = "arm64"
else:
    go_machine = machine
system = platform.system().lower()
actionlint_download_link = f"https://github.com/rhysd/actionlint/releases/download/v{actionlint_version}/actionlint_{actionlint_version}_{system}_{go_machine}.tar.gz"
shellcheck_download_link = f"https://github.com/koalaman/shellcheck/releases/download/v{shellcheck_version}/shellcheck-v{shellcheck_version}.{system}.{machine}.tar.xz"

local_actionlint_archive, headers = urllib.request.urlretrieve(actionlint_download_link)
with tarfile.open(local_actionlint_archive, mode="r:*") as tF:
    edir = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, edir)
    tF.extractall(edir)
    the_actionlint_path = os.path.join(edir, "actionlint")
    # Assuring the right permissions
    os.chmod(the_actionlint_path, 0o555)

local_shellcheck_archive, headers = urllib.request.urlretrieve(shellcheck_download_link)
with tarfile.open(local_shellcheck_archive, mode="r:*") as tF:
    edir = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, edir)
    tF.extractall(edir)
    the_shellcheck_path = os.path.join(edir, f"shellcheck-v{shellcheck_version}", "shellcheck")
    # Assuring the right permissions
    os.chmod(the_shellcheck_path, 0o555)

setup(
    name='pre_commit_placeholder_package',
    version=actionlint_version,
    data_files=[
        ("bin", [the_actionlint_path, the_shellcheck_path])
    ]
)

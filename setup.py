import atexit
import os.path
import platform
from setuptools import setup
import shutil
import tarfile
import tempfile
import urllib.request

setupDir = os.path.dirname(__file__)
with open(os.path.join(setupDir, ".version")) as vH:
    version = vH.read().strip()

machine = platform.machine()
if machine == "x86_64":
    machine = "amd64"
elif machine == "aarch64":
    machine = "arm64"
system = platform.system().lower()
download_link = f"https://github.com/rhysd/actionlint/releases/download/v{version}/actionlint_{version}_{system}_{machine}.tar.gz"
local_filename, headers = urllib.request.urlretrieve(download_link)
with tarfile.open(local_filename, mode="r:*") as tF:
    edir = tempfile.mkdtemp()
    atexit.register(shutil.rmtree, edir)
    tF.extractall(edir)
    the_path = os.path.join(edir, "actionlint")
    # Assuring the right permissions
    os.chmod(the_path, 0o555)

setup(
    name='pre_commit_placeholder_package',
    version=version,
    data_files=[
        ("bin", [the_path])
    ]
)

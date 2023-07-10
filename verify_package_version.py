#!/usr/bin/env python3

import os
import sys

distro = os.popen('cat /etc/os-release | grep "^ID=" | cut -d "=" -f2').read()
if distro.strip() in ("debian", "ubuntu"):
    gramine_expected_version = os.getenv("package_version")
    gramine_installed_version = os.popen("apt-cache policy gramine | grep 'Installed:' | cut -c 14-").read()
else:
    gramine_expected_version = os.getenv("package_version")+"-1"
    gramine_installed_version = os.popen("yum list installed | grep gramine | awk '{print $2}'").read().split(".el")[0]
print("Gramine installed version", gramine_installed_version)
print("Gramine expected version", gramine_expected_version)
if gramine_installed_version.strip() == gramine_expected_version.strip():
    print("versions match")
    sys.exit(0)
else:
    print("Versions don't match")
    raise Exception("Package versions don't match")

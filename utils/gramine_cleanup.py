import subprocess


def cleanup_local_gramine(prefix, os_flavour):
    libdir = subprocess.run("cc -dumpmachine", shell=True, stdout=subprocess.PIPE,
                            encoding="utf-8").stdout.strip()
    arch_libdir = f"/lib/{libdir}"
    if os_flavour == "fedora":
        arch_libdir = "/lib64"
    python_proc = subprocess.run(f"python3 get-python-platlib.py {prefix}", shell=True, stdout=subprocess.PIPE,
                                 encoding="utf-8")
    python_path = python_proc.stdout.strip()
    subprocess.run(f"sudo rm -rf {prefix}/bin/gramine*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/bin/is-sgx-available", shell=True)
    subprocess.run(f"sudo rm -rf {python_path}/*graminelibos*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/*gramine*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libsgx_util.a", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libra_tls_attest.so", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libra_tls_verify.a", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libra_tls_verify_epid.so", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libsecret_prov_attest.so", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libsecret_prov_verify.a", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libsecret_prov_verify_epid.so", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libra_tls_verify_dcap*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/libsecret_prov_verify_dcap.so", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/{arch_libdir}/pkgconfig/*gramine*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/share/doc/gramine*", shell=True)
    subprocess.run(f"sudo rm -rf {prefix}/include/gramine", shell=True)
    print(f"Cleaned Gramine Installation at {prefix}")

def clean_gramine(gramine_path, os_flavour):
    if gramine_path == "/usr":
        pkg_mgr = "apt-get"
        if os_flavour == "fedora":
            pkg_mgr = "yum"
        print("Removing Gramine Installation Using Package Manager")
        subprocess.run(f"sudo {pkg_mgr} autoremove gramine -y > /dev/null", shell=True)
        subprocess.run(f"sudo {pkg_mgr} autoremove gramine-dcap -y > /dev/null", shell=True)

    cleanup_local_gramine(gramine_path, os_flavour)


def get_os_details():
    proc = subprocess.run("grep '^NAME' /etc/os-release", shell=True, stdout=subprocess.PIPE,
                            encoding="utf-8")
    os_details = proc.stdout.strip()
    os_flavour = "ubuntu"
    if ("Ubuntu" not in os_details) and ("Debian" not in os_details):
        os_flavour = "fedora"
    return os_flavour

def check_and_cleanup_gramine():
    os_flavour = get_os_details()
    subprocess.run("wget https://github.com/gramineproject/gramine/raw/master/scripts/get-python-platlib.py",
                   shell=True)
    prefix_path = ["/usr", "/usr/local"]
    for paths in prefix_path:
        clean_gramine(paths, os_flavour)
    while True:
        proc_1 = subprocess.run("which gramine-sgx", shell=True, stdout=subprocess.PIPE,
                                encoding="utf-8")
        output = proc_1.stdout.strip()
        if output in ["", None]:
            break
        print("Gramine Installation Found at : ", output)
        gramine_path = output.split("/bin/gramine-sgx")[0]
        cleanup_local_gramine(gramine_path, os_flavour)
    subprocess.run("sudo rm -rf get-python-platlib.py", shell=True)


if __name__ == "__main__":
    check_and_cleanup_gramine()

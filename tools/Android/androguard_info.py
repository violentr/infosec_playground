# Automate vulnerability research with androguard
# Coded by violentr
# Output: permissions, activities, services, receivers, providers
import os
import sys
from xml.etree import ElementTree as ET

# Redirect stderr entirely during analysis
import contextlib

# Silence the processing output while running custom query
@contextlib.contextmanager
def silence():
    with open(os.devnull, 'w') as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

def exported_components(a):
     # Get manifest as XML string and parse it
    manifest_xml = a.get_android_manifest_axml().get_xml()
    root = ET.fromstring(manifest_xml)

    ns = "http://schemas.android.com/apk/res/android"

    print("\n[!] SECURITY SCAN - EXPORTED COMPONENTS:")

    for tag in ["activity", "service", "receiver", "provider"]:
        for component in root.iter(tag):
            name = component.get(f"{{{ns}}}name", "unknown")
            exported = component.get(f"{{{ns}}}exported", "not set")
            permission = component.get(f"{{{ns}}}permission", None)

            if exported == "true":
                if permission:
                    print(f"  [PROTECTED]  [{tag}] {name} → {permission}")
                else:
                    print(f"  [CRITICAL]   [{tag}] {name} → NO permission!")

def loop_through(subject, collection):
    print(f"\n[+] {subject.upper()}:")
    for item in collection:
        print(item)

def main():
    print("Running your query: \n")
    with silence():
        from androguard.misc import AnalyzeAPK
        a, d, dx = AnalyzeAPK("/Users/admin/Repository/Android/Pulled APK/Chrome64.apk")

    print("[+] Package:", a.get_package())
    loop_through("permissions", a.get_permissions())
    loop_through("activities", a.get_activities())
    loop_through("services", a.get_services())
    loop_through("receivers", a.get_receivers())
    loop_through("providers", a.get_providers())
    exported_components(a)

main()

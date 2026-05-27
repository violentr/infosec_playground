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

def hardcoded_strings(dx):
    print("\n[!] HARDCODED STRINGS:")
    return dx.get_strings()

def dex_class_to_java(class_name):
    if class_name.startswith("L") and class_name.endswith(";"):
        return class_name[1:-1].replace("/", ".")
    return class_name

def get_source_file(class_analysis):
    cls = class_analysis.get_vm_class()
    idx = getattr(cls, "source_file_idx", None)
    if idx is None or idx == 0xFFFFFFFF:
        return None
    return cls.CM.get_string(idx)

def process_hardcoded_strings(strings, dex_list, apk):
    keywords = ["api_key", "secret", "password", "token"]
    vm_to_dex = {id(vm): name for vm, name in zip(dex_list, apk.get_dex_names())}

    for s in strings:
        value = s.get_value()
        if not any(k in value.lower() for k in keywords):
            continue

        print(f"\n[MATCH] String: {value!r}")

        xrefs = s.get_xref_from(with_offset=True)
        if not xrefs:
            print("  (no code references — string exists in pool but may be unused)")
            continue

        for class_analysis, method_analysis, offset in xrefs:
            class_name = class_analysis.name
            method = method_analysis.get_method()
            dex_file = vm_to_dex.get(id(method_analysis.get_vm()), "unknown.dex")
            java_class = dex_class_to_java(class_name)
            source_file = get_source_file(class_analysis)

            print(f"  DEX file:     {dex_file}")
            print(f"  Class:        {class_name}  ({java_class})")
            if source_file:
                print(f"  Source file:  {source_file}")
            print(f"  Method:       {method.get_name()}{method.get_descriptor()}")
            print(f"  Bytecode @:   0x{offset:x}")

def api_permission_usage(a, dx):
    apilevel = a.get_effective_target_sdk_version()
    print(f"\n[!] API PERMISSION USAGE (target SDK {apilevel}):")

    for api_method, perms in dx.get_permissions(apilevel):
        print(f"API: {api_method.full_name}")
        print(f"  permissions: {perms}")
        for _, caller, _ in api_method.get_xref_from():
            print(f"  called from: {caller.full_name}")

def loop_through(subject, collection):
    print(f"\n[+] {subject.upper()}:")
    for item in collection:
        print(item)

def main():
    print("Running your query: \n")
    with silence():
        from androguard.misc import AnalyzeAPK
        if len(sys.argv) < 2:
            print("Usage: python androguard_info.py <path_to_apk>")
            sys.exit(1)

        apk_path = sys.argv[1]

        if not os.path.exists(apk_path):
            print(f"Error: APK file not found: {apk_path}")
            sys.exit(1)

        a, d, dx = AnalyzeAPK(apk_path)
    print("[+] Package:", a.get_package())
    loop_through("permissions", a.get_permissions())
    api_permission_usage(a, dx)
    loop_through("activities", a.get_activities())
    loop_through("services", a.get_services())
    loop_through("receivers", a.get_receivers())
    loop_through("providers", a.get_providers())
    exported_components(a)
    strings = hardcoded_strings(dx)
    process_hardcoded_strings(strings, d, a)

main()

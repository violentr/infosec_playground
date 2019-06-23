# Developed by Deniss Bohanovs aka violentr
# Copyright 2019

#!/usr/bin/env python

import sys, json, subprocess, os, commands, platform
from list_dependencies import ListDependencies
from options_parser import args

OLD_PATH = os.getcwd()
CURRENT_PATH = "."

def set_current_dir():
    global CURRENT_PATH
    try:
        if args.target is not None:
            path = '%s' %(args.target)
            os.chdir(path)
            CURRENT_PATH = args.target
    except OSError as e:
        print("Path was not found: \n %s" % (e.filename))
        sys.exit(1)
    return CURRENT_PATH

class InstallDependencies():

    def __init__(self):
        self.os = self.get_current_os()
        self.dependencies = ListDependencies(self.os).all

    def get_current_os(self):
        try:
            os_name = platform.linux_distribution()[0]
            return {"" : "Os X",
                "Ubuntu" : "Ubuntu",
                "CentOS Linux": "Centos"}[os_name]
        except KeyError:
            print("[-] Found not supported Os - %s" % (os_name))
            sys.exit(1)

    def handle_missing_package(self, command):
        print("----------------------------")
        try:
            subprocess.call(command.split())
        except:
            color_red = "\033[1;31m %s %s %s\033[0m"
            print(color_red % ( "Make sure command: <", command, "> succeeded before continue"))
            sys.exit(1)

    def install_missing_package(self, package):
        package = "".join(package)
        devnull = open(os.devnull, 'w')
        try:
            subprocess.call([package], stdout=devnull, stderr=devnull)
        except OSError as e:
            if e.errno == os.errno.ENOENT:
                current_os = self.os
                selected_package = self.dependencies.get(package, package)
                print("----------------------------")
                print("Current OS: {0}".format(current_os))
                print("Current process: {0}".format(package))
                self.handle_missing_package(selected_package)

                print("----------------------------")
        print("[+] Command '{0}' was succeeded before".format(package))

    def install(self):
        for dependency in self.dependencies.keys():
            self.install_missing_package(dependency)


class JsBughunter():
    def __init__(self):
        self.rows = []
        self.data = self.__run_retire_lib()

    def print_results(self):
        self.__output_result(self.data, self.rows)
        if len(self.data) > 0:
            self.__print_intro()
            self.__print_table(self.rows)
        else:
            print('''
                  ---------------------------------
                  Hooray no bugs found, well done !
                  ---------------------------------
                ''')


#private methods
    def __run_retire_lib(self):
       print("Running retireJS ... ")
       os.system("retire &> /dev/null")

       print("Checking JS libs in %s folder" % CURRENT_PATH)
       vulnerabilities = commands.getoutput("retire --path %s --outputformat json" %(CURRENT_PATH))
       return json.loads(vulnerabilities)

    def __format_bug(self, vulnerability):
        if vulnerability:
            row = [
                    vulnerability['severity'],
                    vulnerability.get('identifiers').get('summary', 'N/A') if vulnerability.get('identifiers', False) else 'N/A',
                    vulnerability['file'] + "\n" + vulnerability.get('info', ['N/A'])[0]
                  ]
            return row

    def __output_result(self, data, rows):
        for item in data:
            for vulnerability in item['results'][0]['vulnerabilities']:
                vulnerability['file'] = item.get('file', 'N/A')
                row = self.__format_bug(vulnerability)
                rows.append(row) if bool(row) else ""

    def __print_intro(self):
        print( """

              /$$$$$  /$$$$$$        /$$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$
             |__  $$ /$$__  $$      | $$__  $$| $$  | $$ /$$__  $$ /$$__  $$
                | $$| $$  \__/      | $$  \ $$| $$  | $$| $$  \__/| $$  \__/
                | $$|  $$$$$$       | $$$$$$$ | $$  | $$| $$ /$$$$|  $$$$$$
           /$$  | $$ \____  $$      | $$__  $$| $$  | $$| $$|_  $$ \____  $$
          | $$  | $$ /$$  \ $$      | $$  \ $$| $$  | $$| $$  \ $$ /$$  \ $$
          |  $$$$$$/|  $$$$$$/      | $$$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/
           \______/  \______/       |_______/  \______/  \______/  \______/


        """)

    def __print_table(self, rows):
            from tabulate import tabulate

            rows = sorted(rows, key=lambda x: x[1])
            headers=['Severity', 'Summary', 'Info']
            print(tabulate(rows, headers=headers, tablefmt='plain'))

if __name__ == "__main__":

    set_current_dir()
    print("Checking for dependecies")
    dependencies = InstallDependencies()
    dependencies.install()

    if os.path.isfile('%s/package.json' % (CURRENT_PATH)):
        dependencies.install_missing_package("npm install")
        dependencies.install_missing_package("pip install -r %s/requirements.txt" % (OLD_PATH))

    print("Checking libraries for JS bugs")
    bug_hunter = JsBughunter()
    bug_hunter.print_results()

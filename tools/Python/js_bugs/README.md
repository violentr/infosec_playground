python version: 2.7.1

Run:

   $ python js_bugs.py --help

Reason:

  Run this script to check js libraries for known vulnerabilities
  with "retire" library, https://github.com/retirejs/retire.js/

Process:

  1. Make sure you install dependencies for your OS by running
  InstallDependencies("Centos") if you have Centos Linux box.
  If no param set it will default to "OS X".

  Supported OS:

  - Ubuntu

  - OS X

  - Centos

  2. When Dependencies successfully installed. Script will run

  "retire" library to analyse installed JS libraries and its contents.

  3. "retire" library's job is to scan JS files inside "node_modules" folder

  and compare them with existing list of known vulnerabilities downloaded from

  "https://raw.githubusercontent.com/RetireJS/retire.js/master/repository/npmrepository.json"

  "https://raw.githubusercontent.com/RetireJS/retire.js/master/repository/jsrepository.json"

  Will output vulnerable version and library if found.

  4. class "InstallDependencies" responsible for installing system dependencies for the

  chosen OS.

  To run script successfully conditions must be satisfied:

  - npm package
  - python-pip package

  5. By default script assumes that none of the listed dependencies were installed.

  But if they are installed, then it outputs message that it was installed.

  6. If for some reason package in the "packages" can not be installed because of the
  dependency for example:

  install "retire" before "npm" then message will be displayed

  "Make sure command <npm install retire> succeeded before continue".
  In this case, to run it smoothly, "npm" must be installed manualy before
  running "npm install retire".

  7. class "JsBughunter" responsibility is to launch "retire" to scan

  JS files and find vulnerabilities, when scan is done output should be

  in json format, no file created.

  8. We use python library "tabulate" to show output in nice, structured way.

  If no output then we congratulate with message "Hooray no bugs found, well done!"

  9. Run vulnerability check in specified folder

     $ python js_bugs.py -d target

#!/usr/bin/env python

import subprocess
interface = raw_input('interface >')
subprocess.call("ifconfig " + interface +"", shell=True)

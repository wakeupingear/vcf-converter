const Indexer = require('friends-js');
const fs = require('fs');
const path = require('path');
const { argv } = require('process');

let contactPath = path.resolve("./contactsInfo.json");
if (contactPath == "/contactsInfo.json") contactPath = path.resolve("/home/pi/personal-site-server/contactsInfo.json");
const contacts = new Indexer(contactPath);
//loop through a file and read each line
const readLine = require('readline');
if (argv.length < 3) {
    console.log("Usage: node import.js <file>");
    process.exit(1);
}
var file = argv[2];
var rl = readLine.createInterface({
    input: fs.createReadStream(file),
    output: process.stdout,
    terminal: false
});
rl.on('line', function (text) {
    contacts.add(text)
});
//timeout
setTimeout(() => {
    rl.close();
    contacts.save();
    console.log("saved");
}, 3000);
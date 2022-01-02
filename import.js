const Indexer = require('friends-js');
const fs = require('fs');
const path = require('path');
const { argv } = require('process');

const prompt = require("prompt-sync")({ sigint: true });

if (argv.length < 3) {
    console.log("Usage: node import.js <file> <optional-args>");
    process.exit(1);
}

let contactPath = path.resolve("./contactsInfo.json");
const username = require("os").userInfo().username;
if (contactPath == "/contactsInfo.json" || username == "pi") contactPath = path.resolve("/home/pi/personal-site-server/contactsInfo.json");
if (argv.includes("--force") && fs.existsSync(contactPath)) {
    fs.unlinkSync(contactPath);
}
const contacts = new Indexer(contactPath);
//loop through a file and read each line
const readLine = require('readline');
var file = argv[2];
var rl = readLine.createInterface({
    input: fs.createReadStream(file),
    output: process.stdout,
    terminal: false
});
rl.on('line', function (text) {
    contacts.add(text)
});
rl.on('close', function () {
    rl.close();
    contacts.save();
    console.log("Final index saved");
    while (true) {
        const query = prompt("Enter a search: ");
        const res = contacts.search(query);
        console.log(res);
    }
});
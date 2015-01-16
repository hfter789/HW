/*
	require 3 arguments, 1 is node, 2 is the file itself,
	3 is the portnum

if(process.argv.length != 3){
	console.log("Error. Usage: node server.js <portnum>");
	return;
}
*/
var PORT = 3333;
var HOST = '127.0.0.1';

var dgram = require('dgram');
var client = dgram.createSocket('udp4');

//message header tests
var message = new Buffer('C461My KungFu is Good!(no good)');

var client = dgram.createSocket('udp4');
client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
});

message = new Buffer('C461BMy KungFu is Good!(no good)');

client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
});

message = new Buffer('  (no good)');

client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
});

message = new Buffer('C4611My KungFu is Good!');

message = new Buffer('C4610103000001211B2D3C4A','hex');


client.send(message, 0, message.length, PORT, HOST, function(err, bytes) {
    if (err) throw err;
    console.log('UDP message sent to ' + HOST +':'+ PORT);
    client.close();
});
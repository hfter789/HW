/*
	require 3 arguments, 1 is node, 2 is the file itself,
	3 is the portnum
*/
if(process.argv.length != 3){
	console.log("Error. Usage: node server.js <portnum>");
	return;
}
//the time that server would wait if not receiving any message from client
var TIMEOUT = 30000
//A magic number & version number in front of the message, discard message if not present
var MAGIC = 0xC461
var VERSION = 1
var MIN_LENGTH = 12 //in bytes
var PORT = process.argv[2];
var HOST = '127.0.0.1';

//create a udp4 server
var dgram = require('dgram');
var server = dgram.createSocket('udp4');
//sessions is a map that maps from session id to # messages the session has received
var sessions = {};

process.stdin.setEncoding('utf8');

process.stdin.on('readable', function() {
  var cmd = process.stdin.read();
  if (cmd && (cmd.toLowerCase() == "q" || cmd.toLowerCase() == "q\n")) {
    process.stdout.write('ByeBye');
    //TODO send all sessions a goodbye message
    process.exit(1);
  }
});

server.on('listening', function () {
    var address = server.address();
    console.log('Waiting on port ' + address.port);
});

server.on('message', function (message, remote) {
    processMsg(message,remote);
});

server.bind(PORT, HOST);

function closeSession(id){
	delete sessions[id];
	console.log("timeout: " + id);
}

function processMsg(message,remote){
    console.log(remote.address + ':' + remote.port +' - ' + message);
    //1)check magic number and version, discard msg if they don't match
	var msg = new Buffer(message);
	//do nothing if the header is not complete or wrong
	if(msg.length < MIN_LENGTH) return;
	console.log("first two bytes are : " + parseInt(msg.slice(0,2).toString('hex',0,2),16) + " MAGIC is : " + MAGIC)
	if(parseInt(msg.slice(0,2).toString('hex',0,2),16)!= MAGIC || msg[2] != VERSION){
		return;
	}
	console.log("MAGIC and VERSION check: PASSED");
	var cmd = msg[3];
	var seqNum = parseInt(msg.slice(4,8).toString('hex',0,4));
	var sesID = msg.slice(8,12).toString('hex',0,4);
	console.log(cmd);
	console.log(seqNum);
	console.log(sesID);

	//2)examines session id: if exist, give to that session, else, create a new session
	if(!(sesID in sessions)){
		sesFields = {};
		sesFields['Timer'] = setTimeout(closeSession, TIMEOUT, sesID);
		sesFields['Address'] = remote;
		sessions[sesID] = sesFields;
	}else{
		sesFields = sessions[sesID];
		if(sesFields && sesFields["Timer"]){
			//resetting the timer
			clearTimeout(sesFields["Timer"]);
			console.log("Timer Cleared");
		}
		sessions[sesID]['Timer'] = setTimeout(closeSession, TIMEOUT, sesID);
	}

	console.log(sessions);
}

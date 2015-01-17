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

//if stdin received input 'q', the program will send goodbye to all alive session
//and exit.
process.stdin.on('readable', function() {
  var cmd = process.stdin.read();
  if (cmd && (cmd.toLowerCase() == "q" || cmd.toLowerCase() == "q\n")) {
    process.stdout.write('ByeBye\n');
    var count = 0;
    for (var key in sessions){
    	console.log(key);
    	closeSession(key);
    	count++;
    }
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

function sendMessage(remote, command, message){
	var newMessage = new Buffer(message).slice(0,MIN_LENGTH);
	newMessage[3] = command;
	console.log("Length of new Message is: " + newMessage.length);
	server.send(newMessage, 0, newMessage.length, remote.port, remote.address, function(err, bytes) {
		if (err) throw err;
		console.log('UDP message sent to ' + remote.address +':'+ remote.port);
	});
}

function closeSession(id){
	message = new Buffer('C461010300000000'+id,'hex');
	var remote = sessions[id]['Address'];
	clearTimeout(sessions[id]['Timer']);
	console.log(remote);
	sendMessage(remote, 3, message);
	delete sessions[id];
	console.log("Session Closed " + id);
}

function resetTimer(id){
	sesFields = sessions[id];
	if(sesFields && sesFields["Timer"]){
		//resetting the timer
		clearTimeout(sesFields["Timer"]);
		console.log("Timer Cleared");
	}
	sessions[id]['Timer'] = setTimeout(closeSession, TIMEOUT, id);
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
	/*
	console.log("Remote is :");
	console.log(remote);
	console.log("Command is :" + cmd);
	console.log("Sequence Number is: "+ seqNum);
	console.log("Session ID is :" + sesID);
	*/
	//2)examines session id: if exist, give to that session, else, create a new session
	if(!(sesID in sessions)){
		if(cmd != 0){
			console.log("Session not created.");
			return;
		}
		sesFields = {};
		sesFields['Timer'] = setTimeout(closeSession, TIMEOUT, sesID);
		sesFields['Address'] = remote;
		sesFields['SeqNum']
		sessions[sesID] = sesFields;
	}else{
		resetTimer(sesID);
	}

	// console.log("Session is :");
	// console.log(sessions);

	if(cmd == 0){
		sendMessage(remote,0,message);
	}else if(cmd == 1){
		console.log("DATA");
		//slice the message to get the payload.
		//payload is everything from the end of header to the end of msg
		var payload = msg.slice(MIN_LENGTH, msg.length);
		process.stdout.write(payload +"\n");
		sendMessage(remote,2,msg);
	}else if(cmd == 2){
		console.log("ALIVE");
		resetTimer(sesID);
	}else if(cmd == 3){
		console.log("GOODBYE");
		closeSession(sesID);
	}else{
		console.log("NOT RECOGNIZED");
		return;
	}


}

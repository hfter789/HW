var dgram = require('dgram');
var util = require('util');


var PORT = 33333;

//-------------------------------------------------
// create datagram (UDP) socket for IPv4 traffic
//-------------------------------------------------
var serverSocket = dgram.createSocket('udp4');

// Fires when socket starts listening for incoming packets.
// We use it only to print an "I'm here" messsage to the console.
serverSocket.on('listening', function () {
    var address = serverSocket.address();
    util.log('UDP Server listening on ' + address.address + ":" + address.port);
});

// Fires when a packet arrives
serverSocket.on('message', function (message, remote) {
    util.log(remote.address + ':' + remote.port +' - ' + message + ' [' + message.toString('hex') + '] ');

    serverSocket.send(message, 0, message.length, remote.port, remote.address);
});

//-------------------------------------------------
// Enable traffic by binding to a port.
// (Not specifying a host/IP in this call means
//  "all IPs for this system".)
//-------------------------------------------------
serverSocket.bind(PORT);

//-------------------------------------------------
// Register stdin handlers
//-------------------------------------------------

// Fires when data is available on stdin.
// (This app doesn't actually use stdin data, except for
// the eof indication.  The 'end' event fires only if 
// you've registered a handler for 'data', though, it seems.)
process.stdin.on('data', function(chunk){
});

// end of file on stdin
process.stdin.on('end', function() {
    util.log('shutdown requested');
    process.exit(0);
});

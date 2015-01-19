/*
Tsz Fung Cheung
CSE461 project 0
client in node.js


*/


var dgram = require('dgram');
var util = require('util');
var crypto = require('crypto');

var TIMEOUT = 30000;

// holds currently active timeout timer, if any
var timer = null;
var state = null; // 0 = hello_wait, 1 = ready, 2 = ready_timer, 3 = closing, 4 = closed
var current_session_id = null;
var last_seq_num = null;
var active = 0;

function generate_session_id() {
  return crypto.randomBytes(4);
};

function timer_on() {
  if ( timer == null ) {
    timer = setTimeout(function() {
      // if not already closing
      if (state != 3) {
        util.log("Times out! closing...");
        say_good_bye();
        state = 3;
      } else {
        util.log("Times out! close now!");
        state = 4;
        process.exit(0);
      }
      
      timer = null;
    }, TIMEOUT);
  }
};

function timer_off() {
  if ( timer ) clearTimeout(timer);
  timer = null;
};

// makes the 12 byte message header from version and command.
// the form "new Buffer('__', 'hex')" is used to create raw bytes from
// hex values. length of the string determines the length of resulting bytes.
// *Note: calling make_header implies sending a packet, and sequence number
// will go up.
function make_header(version, command) {
  var header_magic = new Buffer('c461','hex');
  var header_version = new Buffer(version, 'hex'); // version should be '01'

  var command_code = null;
  switch(command) {
    case 'HELLO':
      command_code = '00';
      break;
    case 'DATA':
      command_code = '01';
      break;
    case 'ALIVE':
      command_code = '02';
      break;
    case 'GOODBYE':
      command_code = '03';
      break;
    default:
      throw 'Invalid command header';
  }
  var header_command = new Buffer(command_code, 'hex'); 

  // first packet.
  if (current_session_id == null && last_seq_num == null) {
    // generate a session_id, copy that to current
    current_session_id = new Buffer(4);
    generate_session_id().copy(current_session_id);
    last_seq_num = 0;
  } else {
    // if only one thing is null, something is wrong.
    if (current_session_id == null || last_seq_num == null) {
      throw 'first packet gone wrong in header!';

    // not first packet.
    } else {
      last_seq_num += 1;
    }
  }

  // here, seq_num is turned into a hex string. Assume that it will not exceed 2 byte.
  var hex_string = last_seq_num.toString(16);

  // padd left with 0s and force it into four bytes(8 chars)
  hex_string = ('0000000' + hex_string).slice(-8);
  var header_seq_num = new Buffer(hex_string, 'hex');
  var header_session = current_session_id;

  // must be in this order.
  var all_headers = [header_magic, header_version, header_command, header_seq_num, header_session];

  // hardcode 12 byte of lenght because it's the protocol.
  return Buffer.concat(all_headers, 12);
};



//------------------------------------------------------
// Set up datagram socket
//------------------------------------------------------


// Obtain server's host from command line arg
if ( process.argv.length != 4 ) {
    util.log("Usage: nodejs client server_name server_port");
    process.exit(1);
}
var serverHost = process.argv[2];
var server_port = process.argv[3];


// create a datagram (UDP) socket, IPv4
var clientSocket = dgram.createSocket('udp4');

function sendMessage(message) {
  clientSocket.send(message, 0, message.length, server_port, serverHost, function(err, bytes) {
    if (err) throw err;
  });
};

// send an initial hello message
var first_hello = make_header('01', 'HELLO');
sendMessage(first_hello);

state = 0; //hello_wait
timer_on();

//------------------------------------------------------
// Set up socket and stdin handlers
//------------------------------------------------------

// When a packet arrives, it must be one of HELLO, ALIVE, GOODBYE
clientSocket.on('message', function(message,remote) {
  // util.log(remote.address + ':' + remote.port +' - ' + message + ' [' + message.toString('hex') + '] ');
  active += 1;
  var hex_message = message.toString('hex');
  

  // ignore message if wrong magic code
  if (hex_message.substring(0,4) !== 'c461') {
    active -= 1;
    return;
  }

  // I speak version 1. receive anything not version 1, ignore.
  if (hex_message.substring(4,6) !== '01') {
    active -= 1;
    return;
  }

  // check what the command is.
  var command_code = hex_message.substring(6,8);

  // HELLO
  if (command_code === '00') {
    // I only expect to see hello in state 'hello_wait'.
    // if I see hello but I'm not in state 0, ignore this message.
    if (state !== 0) {
      active -= 1;
      return;
    } else {
      timer_off();
      state = 1; // Ready
    }

  // ALIVE
  } else if (command_code === '02') {
    // I expect to see ALIVE in state ready, ready timer, and closing.
    
    // ready
    if (state === 1) {
      // do nothing.

    // ready_timer
    } else if (state === 2) {
      state = 1;
      timer_off();

    // closing
    } else if (state) {
      // do nothing.

    // not expecting ALIVE in other states. ignore.
    } else {
      active -= 1;
      return;
    }

  // GOODBYE
  } else if (command_code === '03') {
    // GOODBYE/ in any state transitions to state CLOSED
    state = 4;
    process.exit(0);

  // unknown command. ignore this message.
  } else {
    active -= 1;
    return;
  }
  active -= 1;
});

// When the user types something
process.stdin.on('data', function(chunk) {
  // if user wants to quit
  if (chunk.toString() === 'q\n') {
    process.exit(0);
  }

  // only react to it when we are at state 1 or 2
  if (state !== 1 && state !== 2) {
    return;
  }
  console.log("here")
  active += 1;

  chunk = chunk.toString().trim();

  // seperate lines because sometime input come from files and have \n
  var split = chunk.split('\n');

  for (var i = 0; i < split.length; i++) {
    var message = new Buffer(split[i]);

    var header = make_header('01', 'DATA');
    message = Buffer.concat([header, message], header.length + message.length);

    sendMessage(message);
    // set timer only on 'Ready' state
    if (state === 1) {
      timer_on();
    }
  }

  active -= 1;
});

function say_good_bye() {
  sendMessage(make_header('01', 'GOODBYE'));
};

// On stdin eof, done
process.stdin.on('end', function() { 
    util.log("eof");
    // if not done reading data, wait for a while
    if (active != 0) {
      wait_to_close();
    } else {
      process.exit(0);  
    }
    
});

function wait_to_close() {
  var wait = setTimeout(function() {
    if (active != 0) {
      process.exit(0);
    } else {
      wait_to_close();
    }
  }, 1000);
}







// function debug_log() {
//   util.log('--------vvvvvvv-----');
//   util.log('state: ' + state);
//   util.log('timer: ' + timer);
//   util.log('last_seq_num: ' + last_seq_num);
//   util.log('--------^^^^-----');

// };
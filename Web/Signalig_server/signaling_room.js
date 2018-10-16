"use strict";

// Please install socket.io module
//   npm install socket.io
//
// Run
//   node signaling_room.js

let srv = require('http').Server();
let io = require('socket.io')(srv);
let port = 3002;
let host = null;
let client = null;

srv.listen(port);
console.log('signaling server started on port:' + port);


io.on('connection', function(socket) {
	console.log('-- Socket.io connected --');

	// clientがすでに接続されているかチェック
	socket.on('client', function() {
		if(client != null) {
			io.to(socket.id).emit('notEnter', null);
		}else{
			client = socket.id;
			console.log("client: " + client);
		}
	});

	socket.on('message', function(message) {
		console.log('message: ', message);
		socket.broadcast.emit('message', message);
	});

	// clientの接続が切れたことを他のclientに伝える
	socket.on('disconnect', function(){
		if(client == socket.id){
			client = null;
			socket.broadcast.emit('client disconnect');
			console.log("clinet ")
		}

	});
});

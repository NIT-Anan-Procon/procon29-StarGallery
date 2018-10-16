$(function(){
	let remoteVideo = document.getElementById('remote_video');
	let peerConnection = null;
	var datachannel = null;
	let textToReceiveSdp = null;

	let port = 3002;
	var socket = io.connect('http://localhost:' + port + '/');	// テスト用（多田）
	// var socket = io.connect('https://star-party.anan-nct.ac.jp/');	// 本番用
	socket.on('connect', function(evt) {
		console.log('socket open()');
		socket.emit('client', null);
	});

	socket.on('error', function(err) {
  		console.error('socket error:', err);
	});

	socket.on('notEnter', function(evt) {
		console.log("test");
  		alert("現在は使用できません。\nライブ配信ページへ移動します。");
		document.location.href = "view.html";
	});

	socket.on('message', function(evt) {
		// console.log('socket message data:', evt);
		let message = JSON.parse(evt);
		if (message.type === 'offer') {
			// -- got offer ---
			console.log('Received offer ...');
			textToReceiveSdp = message.sdp;
			let offer = new RTCSessionDescription(message);
			setOffer(offer);
		}
		else if (message.type === 'answer') {
			// --- got answer ---
			console.log('Received answer ...');
			textToReceiveSdp = message.sdp;
			let answer = new RTCSessionDescription(message);
			setAnswer(answer);
		}
		else if (message.type === 'candidate') {
			// --- got ICE candidate ---
			console.log('Received ICE candidate ...');
			let candidate = new RTCIceCandidate(message.ice);
			// console.log(candidate);
			addIceCandidate(candidate);
		}
	});

	function addIceCandidate(candidate) {
		if (peerConnection) {
			peerConnection.addIceCandidate(candidate);
		}
		else {
			console.error('PeerConnection not exist!');
			return;
		}
	}

// --- prefix -----

	RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
	RTCSessionDescription = window.RTCSessionDescription || window.webkitRTCSessionDescription || window.mozRTCSessionDescription;


	function playVideo(element, stream) {
		if ('srcObject' in element) {
			element.srcObject = stream;
		}
		else {
			element.src = window.URL.createObjectURL(stream);
		}
		element.play();
		element.volume = 0;
	}

	function pauseVideo(element) {
		element.pause();
		if ('srcObject' in element) {
			element.srcObject = null;
		}
		else {
			if (element.src && (element.src !== '') ) {
				window.URL.revokeObjectURL(element.src);
			}
			element.src = '';
		}
	}



	function sendSdp(sessionDescription) {
		console.log('---sending sdp ---');

		// --- シグナリングサーバーに送る ---
		let message = JSON.stringify(sessionDescription);
		// console.log('sending SDP=' + message);
		socket.emit('message', message);
	}

	// ---------------------- connection handling -----------------------
	function prepareNewConnection() {
		let pc_config = {"iceServers":[]};
		var peer = new RTCPeerConnection(pc_config);

		// --- on get remote stream ---
		if ('ontrack' in peer) {
			console.log("test1");
			peer.ontrack = function(event) {
				console.log('-- peer.ontrack()');
				let stream = event.streams[0];
				playVideo(remoteVideo, stream);
			};
		}
		else {
			console.log("test2");
			peer.onaddstream = function(event) {
				console.log('-- peer.onaddstream()');
				let stream = event.streams[0];
				playVideo(remoteVideo, stream);
			};
		}

		// --- on get local ICE candidate
		peer.onicecandidate = function (evt) {
			if (evt.candidate) {
				// console.log(evt.candidate);
				sendIceCandidate(evt.candidate);
			} else {
				console.log('empty ice event');
			}
		};
		return peer;
	}

	function sendIceCandidate(candidate) {
		console.log('---sending ICE candidate ---');
		let obj = { type: 'candidate', ice: candidate };
		let message = JSON.stringify(obj);
		console.log('sending candidate=' + message);
		socket.send(message);
}

	function makeOffer() {
		peerConnection = prepareNewConnection();
		datachannel_operate = peerConnection.createDataChannel("operate");
		datachannel_operate.onmessage = function (event) {
			console.log("received: " + event.data);
			document.getElementById('catchData').value += event.data + "\n";
		};
		datachannel_operate.onopen = function () {
			console.log("datachannel_operate open");
		};

		datachannel_operate.onclose = function () {
			console.log("datachannel_operate close");
		};

		peerConnection.createOffer({'OfferToReceiveVideo':true, 'OfferToReceiveAudio':false})
		.then(function (sessionDescription) {
			console.log('createOffer() succsess in promise');
			return peerConnection.setLocalDescription(sessionDescription);
		}).then(function() {
			console.log('setLocalDescription() succsess in promise');
			sendSdp(peerConnection.localDescription);
		}).catch(function(err) {
			console.error(err);
		});
	}

	// not use
	function setOffer(sessionDescription) {
		if (peerConnection) {
			console.error('peerConnection alreay exist!');
		}
		peerConnection = prepareNewConnection();
		peerConnection.setRemoteDescription(sessionDescription)
		.then(function() {
			console.log('setRemoteDescription(offer) succsess in promise');
			makeAnswer();
		}).catch(function(err) {
			console.error('setRemoteDescription(offer) ERROR: ', err);
		});
	}

	// not use
	function makeAnswer() {
		console.log('sending Answer. Creating remote session description...' );
		if (! peerConnection) {
			console.error('peerConnection NOT exist!');
			return;
		}

		peerConnection.createAnswer()
		.then(function (sessionDescription) {
			console.log('createAnswer() succsess in promise');
			return peerConnection.setLocalDescription(sessionDescription);
		}).then(function() {
			console.log('setLocalDescription() succsess in promise');
			peerConnection.ondatachannel = function(evt) {
				datachannel_operate = evt.channel;
				datachannel_operate.onmessage = function (event) {
					console.log("received: " + event.data);
					document.getElementById('catchData').value += event.data + "\n";
				};
				datachannel_operate.onopen = function () {
					console.log("datachannel_operate open");
				};
				datachannel_operate.onclose = function () {
					console.log("datachannel_operate close");
				};
			}
			sendSdp(peerConnection.localDescription);
		}).catch(function(err) {
			console.error(err);
		});
	}

	function setAnswer(sessionDescription) {
		if (! peerConnection) {
			console.error('peerConnection NOT exist!');
			return;
		}

		peerConnection.setRemoteDescription(sessionDescription)
		.then(function() {
			console.log('setRemoteDescription(answer) succsess in promise');
		}).catch(function(err) {
			console.error('setRemoteDescription(answer) ERROR: ', err);
		});
	}

	function sendData(string){
		datachannel_operate.send(string);
		console.log('Sent Data: ' + string);
	}

	$('#push').click(function(){
		let data = $('#pushData').val();
		sendData(data);
		$('#pushData').val("");
	});

	$('#speed, #focus').change(function(){
		let val = $(this).val();
		sendData(val);
	});

	$('#up').click(function(){
		sendData('up');
	});

	$('#left').click(function(){
		sendData('left');
	});

	$('#right').click(function(){
		sendData('right');
	});

	$('#down').click(function(){
		sendData('down');
	});

	$('#wide_angle').click(function(){
		sendData('wide_angle');
	});

	$('#telephoto').click(function(){
		sendData('telephoto');
	});

	// start PeerConnection
	$('#connect').click(function(){
		if (! peerConnection) {
			console.log('make Offer');
			makeOffer();
		}
		else {
			console.warn('peer already exist.');
		}
	});

	// close PeerConnection
	$('#hangUp, #wide_angle, #telephoto').click(function(){
		if (peerConnection) {
			console.log('Hang up.');
			peerConnection.close();
			peerConnection = null;
			pauseVideo(remoteVideo);
		}
		else {
			console.warn('peer NOT exist.');
		}
	});
});

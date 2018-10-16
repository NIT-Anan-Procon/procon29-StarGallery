let startVideo;
let stopVideo;
let connect;
let hangUp;
let pushText;
window.addEventListener('load', function(){
	const localVideo = document.getElementById('telephoto');
	let localStream = [];
	localStream[0] = null;
	localStream[1] = null;
	let peerConnection = null;
	let datachannel = null;
	let textToReceiveSdp = null;
	let camera = "wide_angle";


	// signaling serverと接続
	let port = 3002;
	// var socket = io.connect('https://star-party.anan-nct.ac.jp' + '/'); //本番用
	let socket = io.connect('http://localhost:' + port + '/'); // ローカルテスト用
	socket.on('connect', function (evt) {
		printLog('socket open');
	});
	socket.on('error', function (err) {
		printLog("error:" + 'socket error:', err);
	});

	socket.on('message', function (evt) {
		// printLog('socket message data:', evt);
		let message = JSON.parse(evt);
		if (message.type === 'offer') {
			// -- got offer ---
			printLog('Received offer ...');
			textToReceiveSdp = message.sdp;
			let offer = new RTCSessionDescription(message);
			setOffer(offer);
		}
		else if (message.type === 'answer') {
			// --- got answer ---
			printLog('Received answer ...');
			textToReceiveSdp = message.sdp;
			let answer = new RTCSessionDescription(message);
			setAnswer(answer);
		}
		else if (message.type === 'candidate') {
			// --- got ICE candidate ---
			printLog('Received ICE candidate ...');
			let candidate = new RTCIceCandidate(message.ice);
			printLog(candidate);
			addIceCandidate(candidate);
		}
	});

	function addIceCandidate(candidate) {
		if (peerConnection) {
			peerConnection.addIceCandidate(candidate);
		}
		else {
			printLog("error:" + 'PeerConnection not exist!');
			return;
		}
	}

	// canvasにカメラから送られてくる画像を表示
	const canvas = document.getElementById('wide_angle');
	const ctx = canvas.getContext('2d');
	const img = new Image();
	let count = 1; // カメラ未接続用
	try{
		// canvasからstream取得
		localStream[0] = canvas.captureStream(15);
		printLog("Get canvasStream.");
	} catch {
		printLog("Faild to get canvasStream.");
	}
	function reload(){
	  if ( ! canvas || ! canvas.getContext ) { return false; }
	  /* Imageオブジェクトを生成 */
	  img.src = "./data" + count + ".jpg?r=" + Math.random(); // カメラ未接続用 本番はcountを消す
	  if(count >= 75){
		count = 1;
	  }else{
		count++;
	  }
	  /* 画像が読み込まれるのを待ってから処理を続行 */
	  img.onload = function() {
		ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
	  }
	}
	setInterval(reload,33);





	// --- prefix -----
	navigator.getUserMedia = navigator.getUserMedia || navigator.webkitGetUserMedia ||
	navigator.mozGetUserMedia || navigator.msGetUserMedia;
	RTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection || window.mozRTCPeerConnection;
	RTCSessionDescription = window.RTCSessionDescription || window.webkitRTCSessionDescription || window.mozRTCSessionDescription;

	// ---------------------- media handling -----------------------
	// start local video
	startVideo = function() {

		let camera_id = null;
		// deviceのidを表示
		navigator.mediaDevices.enumerateDevices().then(function(devices) {
			devices.forEach(function(device) {
				// printLog(device.kind + ": " + device.label + " id = " + device.deviceId); // デバイスの情報を表示
				if(device.label == "SKYRIS 618M (199e:8441)") {
					camera_id = device.deviceId;
				}
			});

			// 取得したカメラIDを登録
			const mediaoption = {video:{deviceId: camera_id}, audio: false};	//skyris618M

			getDeviceStream(mediaoption)
			.then(function (stream) { // success
				localStream[1] = stream;
				playVideo(localVideo, stream);
			}).catch(function (error) { // error
				printLog("error:" + 'getUserMedia error:', error);
				return;
			});
		});
	}

	// stop local video
	stopVideo = function () {
		pauseVideo(localVideo);
		stopLocalStream(localStream[0]);
		stopLocalStream(localStream[1]);
	}

	function stopLocalStream(stream) {
		let tracks = stream.getTracks();
		if (!tracks) {
			printLog("warn:" + 'NO tracks');
			return;
		}
		for (let track of tracks) {
			track.stop();
		}
	}

	function getDeviceStream(option) {
		if ('getUserMedia' in navigator.mediaDevices) {
			printLog('navigator.mediaDevices.getUserMadia');
			return navigator.mediaDevices.getUserMedia(option);
		}
		else {
			printLog('wrap navigator.getUserMadia with Promise');
			return new Promise(function (resolve, reject) {
				navigator.getUserMedia(option, resolve, reject);
			});
		}
	}

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
			if (element.src && (element.src !== '')) {
				window.URL.revokeObjectURL(element.src);
			}
			element.src = '';
		}
	}


	function sendSdp(sessionDescription) {
		printLog('---sending sdp ---');

		// --- シグナリングサーバーに送る ---
		let message = JSON.stringify(sessionDescription);
		// printLog('sending SDP=' + message);
		socket.emit('message', message);
	}

	// ---------------------- connection handling -----------------------
	function prepareNewConnection() {
		let pc_config = { "iceServers": [] };
		var peer = new RTCPeerConnection(pc_config);

		// --- on get remote stream ---
		if ('ontrack' in peer) {
			peer.ontrack = function (event) {
				printLog('-- peer.ontrack()');
			};
		}
		else {
			peer.onaddstream = function (event) {
				printLog('-- peer.onaddstream()');
			};
		}

		// --- on get local ICE candidate
		peer.onicecandidate = function (evt) {
			if (evt.candidate) {
				printLog(evt.candidate);
				// Trickle ICE の場合は、ICE candidateを相手に送る
				sendIceCandidate(evt.candidate);
				// Vanilla ICE の場合には、何もしない
			} else {
				printLog('empty ice event');
			}
		};


		// -- add local stream --
		if (localStream[0] && camera == "wide_angle") {
			printLog('Adding local stream...');
			peer.addStream(localStream[0]);
		}

		else if(localStream[1] && camera == "telephoto"){
			printLog('Adding local stream...');
			peer.addStream(localStream[1]);
		}
		else {
			printLog("warn:" + 'no local stream, but continue.');
		}
		return peer;
	}

	function sendIceCandidate(candidate) {
		printLog('---sending ICE candidate ---');
		let obj = { type: 'candidate', ice: candidate };
		let message = JSON.stringify(obj);
		// printLog('sending candidate=' + message);
		socket.send(message);
}

	function makeOffer() {
		peerConnection = prepareNewConnection();
		datachannel = peerConnection.createDataChannel("operate");
		datachannel.onmessage = function (event) {
			const textarea_id = 'catchDataList';
			addStringToTextarea(textarea_id, event.data);
			// websocket.send(event.data);
			if(event.data == "telephoto" || event.data == "wide_angle"){
				if(event.data == "telephoto"){
					camera = "telephoto";
					hangUp();
					connect();
				}
				else {
					camera = "wide_angle";
					hangUp();
					connect();
				}
			}
		};
		datachannel.onopen = function () {
			printLog("datachannel open");
		};

		datachannel.onclose = function () {
			printLog("datachannel close");
		};


		peerConnection.createOffer()
		.then(function (sessionDescription) {
			printLog('createOffer() succsess in promise');
			return peerConnection.setLocalDescription(sessionDescription);
		}).then(function () {
			printLog('setLocalDescription() succsess in promise');

			// -- Trickle ICE の場合は、初期SDPを相手に送る --
			// -- Vanilla ICE の場合には、まだSDPは送らない --
			sendSdp(peerConnection.localDescription);
		}).catch(function (err) {
			printLog("error:" + err);
		});
	}

	function setOffer(sessionDescription) {
		if (peerConnection) {
			printLog("error:" + 'peerConnection alreay exist!');
		}
		peerConnection = prepareNewConnection();
		peerConnection.setRemoteDescription(sessionDescription)
		.then(function () {
			printLog('setRemoteDescription(offer) succsess in promise');
			makeAnswer();
		}).catch(function (err) {
			printLog("error:" + 'setRemoteDescription(offer) ERROR: ', err);
		});
	}

	function makeAnswer() {
		printLog('sending Answer. Creating remote session description...');
		if (!peerConnection) {
			printLog("error:" + 'peerConnection NOT exist!');
			return;
		}

		peerConnection.createAnswer()
		.then(function (sessionDescription) {
			printLog('createAnswer() succsess in promise');
			return peerConnection.setLocalDescription(sessionDescription);
		}).then(function () {
			printLog('setLocalDescription() succsess in promise');
			peerConnection.ondatachannel = function (evt) {
				datachannel = evt.channel;
				datachannel.onmessage = function (event) {
					printLog("received: " + event.data);
					document.getElementById('catchDataList').value += event.data + "\n";
					if(event.data == "telephoto" || event.data == "wide_angle"){
						if(event.data == "telephoto"){
							room = "telephoto";
							hangUp();
							stopVideo();
							startVideo();
							connect();
						}
					}
				};
				datachannel.onopen = function () {
					printLog("datachannel open");
				};

				datachannel.onclose = function () {
					printLog("datachannel close");
				};
			}

			sendSdp(peerConnection.localDescription);
		}).catch(function (err) {
			printLog("error:" + err);
		});
	}

	function setAnswer(sessionDescription) {
		if (!peerConnection) {
			printLog("error:" + 'peerConnection NOT exist!');
			return;
		}

		peerConnection.setRemoteDescription(sessionDescription)
		.then(function () {
			printLog('setRemoteDescription(answer) succsess in promise');
		}).catch(function (err) {
			printLog("error:" + 'setRemoteDescription(answer) ERROR: ', err);
		});
	}

	pushText = function() {
		let data = document.getElementById('pushData');
		datachannel.send(data.value);
		printLog('Sent Data: ' + data.value);
		data.value = "";
	}

	// start PeerConnection
	connect = function () {
		if (!peerConnection) {
			printLog('make Offer');
			makeOffer();
		}
		else {
			printLog("warn:" + 'peer already exist.');
		}
	}

	// close PeerConnection
	hangUp = function () {
		if (peerConnection) {
			printLog('Hang up.');
			peerConnection.close();
			peerConnection = null;
		}
		else {
			printLog("warn:" + 'peer NOT exist.');
		}
	}

	// startVideo();
});

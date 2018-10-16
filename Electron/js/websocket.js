const url = 'localhost:1996';
let webSocket = null;

function open(){
	if(webSocket == null){
		webSocket = new WebSocket(url);

		// イベントハンドラの設定
		webSocket.onopen = onOpen;
		webSocket.onmessage = onMessage;
		webSocket.onclose = onClose;
		webSocket.onerror = onError;
	}
}

// 接続イベント
function onOpen(event){
	printLog("接続に成功しました。");
}
// メッセージ受信イベント
function onMessage(event) {
	if (event && event.data) {
		printLog(event.data);
	}
}
// エラーイベント
function onError(event) {
	console.error("エラーが発生しました。");
}
// 切断イベント
function onClose(event) {
	printLog("切断しました。3秒後に再接続します。(" + event.code + ")");
	webSocket = null;
	setTimeout("open()", 3000);
}

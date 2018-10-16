// サーバとの接続
var socketio = io();

// 接続後の処理
$(function(){
	$('#message_form').submit(function(){
		// コメントを送信
		socketio.emit('Mymessage', $('#message').val());
		$('#message').val('');
		return false;
	});
	// コメントを受信したときの処理
	socketio.on('message', function(message){
		// コメントをページに追加す
		$('#chatArea').val($('#chatArea').val() + message + "\n");
		// テキストエリアを一番下までスクロールする
		$('#chatArea').animate({scrollTop: $('#chatArea')[0].scrollHeight}, 'fast');
	});
});

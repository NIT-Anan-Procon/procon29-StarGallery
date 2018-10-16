// 関数を保存する変数の用意
let printLog;
let addStringToTextarea;

window.addEventListener('DOMContentLoaded', function() {


	// ログを表示する
	printLog = function() {
		let textarea_id = 'logList';
		let string = "";
		for(let i = 0; i < arguments.length; i++){
			string += arguments[i];
		}
		addStringToTextarea(textarea_id, string);
	};

	// 送られてきたデータを画面に表示
	function printData(string){
		let textarea_id = 'catchDataList';
		// let string = "";
		// for(let i = 0; i < arguments.length; i++){
		// 	string += arguments[i];
		// }
		addStringToTextarea(textarea_id, string);
	}

	// テキストエリアに文字を追加
	addStringToTextarea = function (id, string){
		const area = document.getElementById(id);
		area.value += string + "\n";
		// テキストエリアを一番下までスクロールする
		area.scrollTop = area.scrollHeight;
	}


});

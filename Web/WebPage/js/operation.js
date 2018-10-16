$(function(){
	let minutes = 10;
	let seconds = 0;

	const time_show = function(){
		$('#time_limit').val(
			((minutes < 10) ? "0" + minutes : minutes) + ':' +
			((seconds < 10) ? "0" + seconds : seconds)
		);
	}

	time_show();

	let countdown = function(){
		if (seconds == 0) {
			if(minutes == 0){
				// alert("Time UP");
				// history.back(-1);
			} else{
				minutes--;
				seconds = 59;
			}
		}
		else {
			seconds--;
		}

		time_show();
	}
	setInterval(countdown, 1000);
});

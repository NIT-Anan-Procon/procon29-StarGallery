// イメージマップのレスポンシブな画像対応
$('#map').rwdImageMaps();


// イメージマップイベント
$(function() {
  // ポップアップ表示
  $('.city').hover(function(event) {
    $('.popup').css({
      'left' : event.offsetX +  'px',
      'top' : event.offsetY  + 'px'
    });
    $('.popup').show();
  }, function() {
    $('.popup').hide();
  });

  //モーダルウィンドウ

  $('.city').click(function(){
	$(this).blur();
	//↓新しくモーダルウィンドウを起動しない
	if($('#modal-overlay')[0]) return false;
	$('body').append('<div id="modal-overlay"></div>');
	$('#modal-overlay').fadeIn('slow');

	centeringModalSyncer();

	$('#modal-content').fadeIn('slow');

	$('#modal-overlay').unbind().click(function(){
	  $('#modal-overlay,#modal-content').fadeOut('slow',function(){
		$('#modal-overlay').remove();
	  });
	});
  });

$(window).resize(centeringModalSyncer);
	function centeringModalSyncer(){
		var w = $( window ).width() ;
		var h = $( window ).height() ;
		var cw = $( "#modal-content" ).outerWidth();
		var ch = $( "#modal-content" ).outerHeight();

		$( "#modal-content" ).css( {"left": ((w - cw)/2) + "px","top": ((h - ch)/2) + "px"} ) ;
	}
});

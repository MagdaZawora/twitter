$(document).ready(function() {
	$('.panel').on('click', function() {
	    $('.panel').hide();
	});
	$('.page-header').fadeIn(1000);
	$('#test').on('click', function(event) {
	    alert('Ćwierknąłeś twita!');
	});
});

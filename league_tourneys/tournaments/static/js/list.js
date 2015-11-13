$(document).ready(function(){
	$('tr').click(function(){
		window.location.href = $(this).find("a").attr("href");
	});
});

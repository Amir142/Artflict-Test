$(document).ready(function(){

	$(".menu_item#home").on("click", function(){
		window.location = "/feed";
	});
	$(".menu_item#profile").on("click", function(){
		window.location = "/profile";
	});
	$(".menu_item#add_post").on("click", function(){
		window.location = "/add";
	});

});


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
	$(".menu_item#log_out").on("click", function(){
		window.location = "/logout";
	});

	$(".modal_bg").on("click", function(e){
		if(e.target.className.includes("modal_bg")){
			close_modals();
		}
	});

});

function close_modals(){
	$(".modal_bg").css("display", "none");
	$(".modal").css("display", "none");
}

function open_modal(id){
	$("#" + id).css("display", "block");
	$(".modal_bg").css("display", "flex");
}
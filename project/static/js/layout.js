
$(document).ready(function(){

	close_modals();

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
	$(".modal").css("display", "none");
	$(".modal_bg").css("display", "none");
	$("#delete_post_confirm_form")[0].reset();
	$("#upload_art_form")[0].reset();
}

function open_modal(id){
	$("#" + id).css("display", "block");
	$(".modal_bg").css("display", "flex");
}
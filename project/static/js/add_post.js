$(document).ready(function(){

	$("#add_title").on('focus', function(){
		$("#add_title").removeClass('warning');
	});

	$("#add_text").on('focus', function(){
		$("#add_text").removeClass('warning');
	});

	$("#submit_button").on('click', function(){
		validate_post();
	});

});

function validate_post(){

	let title = $("#add_title").val();
	let text = $("#add_text").val();
	let post = true;

	if(title === ""){
		$("#add_title").addClass("warning");
		post = false;
	};

	if(text === ""){
		$("#add_text").addClass("warning");
		post = false;
	};

	return post;
};



var urlParams = new URLSearchParams(window.location.search);

$(document).ready(function(){
	$("select#sort_options_list").on("change", function(){
		let key = $("select#sort_options_list").val();
		urlParams.set("sort_by", key);
		window.location.search = urlParams.toString();
	});

	$("select#show_options_list").on("change", function(){
		let key = $("select#show_options_list").val();
		urlParams.set("show", key);
		window.location.search = urlParams.toString();
	});

	$("#reverse_order").on("click", function(){
		if(urlParams.get("order") == "normal"){
			urlParams.set("order", "reverse");
		}
		else if(urlParams.get("order") == "reverse"){
			urlParams.set("order", "normal");
		}
		window.location.search = urlParams.toString();
	});

	$(".post_template").on("click",function(e){
		let template = get_template(e.target);
		let id = template.id.substring(8);
		let classes = e.target.className;

		if(!(classes.includes("relate_button") || classes.includes("delete_button")))
		{
			window.location.href = "/stories/" + id;
		}
	});

	select_dropdown_options();

});


function get_template(element){
	if(element.className.includes("post_template")){
		return element;
	}
	return get_template(element.parentNode);
};

function select_dropdown_options(){

	if(!urlParams.has("sort_by")){
		urlParams.append("sort_by", "new");
	}

	if(!urlParams.has("show")){
		urlParams.append("show", "all");
	}

	if(!urlParams.has("order")){
		urlParams.append("order", "normal");
	}

	let sort_by = urlParams.get("sort_by");
	let show = urlParams.get("show");
	$("select#sort_options_list").val(sort_by);
	$("select#show_options_list").val(show);

};

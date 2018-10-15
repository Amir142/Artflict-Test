

var urlParams = new URLSearchParams(window.location.search);
var sort_list = {"new": "New","top":"Top","alphabetical":"A-Z"};
var show_list = {"all":"All","artless":"Artless","with-art":"With Art"};

$(document).ready(function(){

	select_dropdown_options();

	$("select#sort_options_list").on("change", function(){
		let key = $("select#sort_options_list").val();
		console.log(key);
		urlParams.set("sort_by", key);
		window.location.search = urlParams.toString();
	});

	$("select#show_options_list").on("change", function(){
		let key = $("select#show_options_list").val();
		console.log(key);
		urlParams.set("show", key);
		window.location.search = urlParams.toString();
	});

	$(".post_template").on("click",function(e){

		let template = get_template(e.target);
		let id = template.id.substring(8);

		if(!e.target.className.includes("relate_button"))
		{
			window.location.href = "/stories/" + id;
		}
	});
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

	let sort_by = urlParams.get("sort_by");
	let show = urlParams.get("show");
	console.log(sort_list[sort_by]);
	$("select#sort_options_list").val(sort_list[sort_by].toString());
	$("select#show_options_list").val(show_list[show].toString());

};

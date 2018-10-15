
$(document).ready(function(){
	$(".relate_button").on("click", function(e){
		let id = e.target.id.substring(10);
		relate(id);
	});
});

function set_relate_color(like, is_liked){
        if(is_liked === "yes"){
			$(like).attr("src",full_heart);
        }
        else{
			$(like).attr("src",empty_heart);
		}
};

function relate(id){
    let button = document.getElementById("relate_no_" + id);

    $.ajax({
		type: "POST",
		url: '/relate/' + id.toString(),
		success: function(response){
			console.log(response);
			response = JSON.parse(response);
		  	console.log(response);
		  	message = response.message;
			if(message === "like added"){
			  set_relate_color(button, "yes");
			}

			else if(message === "like removed"){
			  set_relate_color(button, "no");
			}

			$("#like_number").text(response.likes);

	    },
		error: function(response){
			console.log("error");
		}

    });

};

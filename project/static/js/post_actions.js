
$(document).ready(function(){

	$(".delete_button").on("click", function(e){		
		let id = e.target.id.substring(10);

		open_modal("confirm_delete_modal");
	
		$("#delete_post_confirm").on("click", function(e){
			delete_post(id);
		});

	});

	$(".relate_button").on("click", function(e){
		let id = e.target.id.substring(10);
		relate(id);
	});

	$(".illustrate_button").on("click", function(e){

		let id = e.target.id.substring(14);
		
		$('#upload_art_modal').attr('action', 'illustrate/' + id);

		open_modal("upload_art_modal");

		$("#delete_post_cancel").on("click", function(e){
			close_modals();
		});
	
		$("#delete_post_confirm").on("click", function(e){
			delete_post(id);
		});

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

function delete_post(id){
	console.log("delete " + id);
	
	$.ajax({
		type: "POST",
		url: '/delete/' + id,
		success: function(){			
			if(window.location.includes("feed"))
			{
				window.location.reload();
			}
			else{
				window.location = "/feed";
			}
		},
		error: function(response){
			console.log(response);
		}
	});
}

function relate(id){
    let button = document.getElementById("relate_no_" + id);

    $.ajax({
		type: "POST",
		url: '/relate/' + id,
		success: function(response){
			response = JSON.parse(response);
		  	message = response.message;
			if(message === "like added"){
			  set_relate_color(button, "yes");
			}

			else if(message === "like removed"){
			  set_relate_color(button, "no");
			}

			$("#like_number_" + id).text(response.likes);

	    },
		error: function(response){
			console.log(response);
		}

    });

};

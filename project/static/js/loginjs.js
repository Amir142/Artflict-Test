

$( document ).ready(function() {

	$("#switch_to_signup").on("click", function(){
		console.log("to signup");
		open_signup_form();
	});

	$("#switch_to_login").on("click", function(){
		console.log("to login");
		open_login_form();
	});


	let show = getdata["show"];
	if(show == null){
		show = 'login';
	}

	let warning = getdata["err_msg"];
	if(warning != null){

		let warning_color = "rgb(240,0,0)"


		//signup warning(s)
		if(warning == "username cannot be empty"){
			let textbox = document.getElementById("signup_textbox_username");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("username_error_message");
			message.innerText = "Username cannot be empty.";
			message.style["display"] = "block";
		}

		if(warning == "display name cannot be empty"){
			let textbox = document.getElementById("signup_textbox_displayname");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("displayname_error_message");
			message.innerText = "Display name cannot be empty.";
			message.style["display"] = "block";
		}

		if(warning == "password cannot be empty"){
			let textbox = document.getElementById("signup_textbox_password");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("password_err_msg");
			message.innerText = "Password cannot be empty.";
			message.style["display"] = "block";
		}

		if(warning == "name taken"){
			let textbox = document.getElementById("signup_textbox_username");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("username_error_message");
			message.innerText = "username is taken";
			message.style["display"] = "block";
		}

		if(warning == "passwords do not match"){
			let textbox = document.getElementById("signup_textbox_password_confirm");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("pass_dont_match_msg");
			message.innerText = "Passwords do not match.";
			message.style["display"] = "block";
		}

		//login warning(s)
		if(warning == "wrong username or pass"){
			let textbox = document.getElementById("login_textbox_username");
			textbox.style["border-color"] = warning_color;
			let message = document.getElementById("wrong_cred_msg");
			message.innerText = "Wrong username or password.";
			message.style["display"] = "block";
		}

	}

});

function open_signup_form(){
	let form = $("#login_form").trigger("reset");
	window.location.href = "/register";
}

function open_login_form() {
	let form = $("#signup_form").trigger("reset");
	window.location.href = "/login";
}

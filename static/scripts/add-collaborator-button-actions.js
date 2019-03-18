
function respond(){
	//console.log("respond");
	data = {"message1":"John", "message2":"Doe"}
	var formData = new FormData(document.getElementById('collabs-recieved-form'))
	
	for(var pair of formData.entries()) {
		console.log(pair[0]+ ', '+ pair[1]); 
	}

	$.ajax({
		type: "POST",
		url: "http://localhost:8000/kollab/collabs/respond/",
		processData: false,
		contentType: false,
		data: formData		
	})
}	

function sendRequest(){
	console.log("send request");
	data = {"message1":"John", "message2":"Doe"}
	var formData = new FormData(document.getElementById('add-collaborator-form'))
	
	for(var pair of formData.entries()) {
		console.log(pair[0]+ ', '+ pair[1]); 
	}
	
	$.ajax({
		type: "POST",
		url: "http://localhost:8000/kollab/collabs/init/",
		processData: false,
		contentType: false,
		data: formData		
	})
}	

function changeColour(){
	$("#send-collab-button").addClass('btn-success').removeClass('btn-primary').text("Request Sent");	
}

function collabSent(status){
	text = "based on bool"
	console.log("collabsent")
	if(status == "CONF"){
		text="Collaborators"
	
	}else{
		text="Request Pending"
	}
	
	console.log(status)
	
	$("#send-collab-button").prop('onclick', null).addClass('btn-success').removeClass('btn-primary').text(text);	
}
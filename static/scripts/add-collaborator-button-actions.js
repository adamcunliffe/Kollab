
function confirm(){
	console.log("confirm");
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
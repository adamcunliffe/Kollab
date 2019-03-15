function signUpData(){
	var formElems = document.getElementById("signupForm").elements;
	
	var formData = {}
	var checkedTags = [];
	for(var i = 0; i < formElems.length ; i++){
		var item = formElems.item(i);
		//console.log(item.value)
		formData[item.name] = item.value;
		
		if(item.name == 'tags' && item.checked == true){
			checkedTags.push(item.value);
			
		}		
	}
	
	formData['tags'] = checkedTags;

	//console.log(JSON.stringify(formData));
	
	var latLon = {}
	
	if("geolocation" in navigator){
		navigator.geolocation.getCurrentPosition(function(position){
			console.log(position.coords.latitude, position.coords.longitude);
			latLon['lat'] = position.coords.latitude;
			latLon['lon'] = position.coords.longitude;
			formData['latLon'] = latLon;
			console.log(JSON.stringify(formData));
			postData(JSON.stringify(formData));
		});
	}else{
		postData(JSON.stringify(formData));
		console.log("geo not available")
	}
	
	//console.log(JSON.stringify(formData));
	
}

function postData(formData){
	$.ajax({
		type: "POST",
		url: "http://localhost:8000/kollab/submitSignUp/",
		data: formData,
		beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", formData['csrfmiddlewaretoken']);
        }
	}).done(function(){
		console.log("success");
	}).fail(function(){
		console.log("fail");
	});
}







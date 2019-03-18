$(document).ready(function(){ 
	$.ajax({
		type: "GET",
		url: "http://api.icndb.com/jokes/random?escape=javascript"
	}).done(function(data){
		console.log(JSON.stringify(data))
		console.log(data['value']['joke'])
		$("#short").text(data['value']['joke'])
	});
 });
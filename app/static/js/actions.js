window.onload = function(){
	console.log('Alles kaputt');

}

function deleteFriend(id){

	var r = confirm("You want to delete selected item?");
	if(r){
		var xhttp = new XMLHttpRequest();
		xhttp.onreadystatechange = function() {
			if (xhttp.readyState == 4 && xhttp.status == 200) {

				window.location.href = window.location.href;
			}
		}

		xhttp.open("GET", "/delete/" + id, true);
		xhttp.send();
	}
}

function updateFriend(id){
	console.log('Update friend function called with value' + id);
	

	console.log(id);
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && xhttp.status == 200) {
			document.write(xhttp.responseText)
		}
	}
		
	xhttp.open("GET", "/update/" + id, true);
	xhttp.send();
	return false;
}
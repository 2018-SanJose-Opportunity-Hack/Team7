login = function(){
	var password = document.getElementById("password").value;
    var email = document.getElementById("email").value;
    var url = app_url + "/processlogin?password="+password+"&email="+email;
    sendAjaxRequest(url,loginCallBack);
}

loginCallBack = function(statusCode){
if(statusCode == successStatusCode){
    window.location.href = app_url+"/home";
}
else{
    alert("Invalid Credentials");
}  
}


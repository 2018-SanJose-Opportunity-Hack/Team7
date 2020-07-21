var Client = require('node-rest-client').Client;
var client = new Client();
var successStatusCode = 200;
var request = require("request");

var defaultPostArgs = {
          headers: { "Content-Type": "application/json" }
  };

module.exports = {

	sendRestPostRequest : function(url,args,callback,req,res){
		console.log(url);
		console.log(JSON.stringify(args));
		// client.post(url,args, function (data, response) {
		//     callback(data,response.statusCode,req,res);
		// });
		
		var options = { method: 'POST',
		  url: url,
		  headers: 
		   {'cache-control': 'no-cache' },
		  body: JSON.stringify(args) };

		request(options, function (error, response, body) {
		  if (error) throw new Error(error);

		  callback(body,response.statusCode,req,res);
		});

	},

	sendRestGetRequest : function(url,callback,req,res){

		var options = { method: 'GET',
						  url: url,
						  headers: 
						   {'content-type': 'application/json' } };


		request(options, function (error, response, body) {
		  if (error) throw new Error(error);
		  callback(body,response.statusCode,req,res);
		  console.log(body);
		});

	},
	sendRestPutRequest : function(url,args,callback,req,res){

		var options = { method: 'PUT',
						  url: url,
						  headers: 
						   {'content-type': 'application/json' },
						   body: JSON.stringify(args)  };

						   console.log(options);
		request(options, function (error, response, body) {
		  if (error) throw new Error(error);
		  callback(body,response.statusCode,req,res);
		  console.log(body);
		});

	}
}

loginPostCallback = function(data,statusCode,req,res){
    console.log(data);
    //console.log(JSON.parse(data).id);
    console.log(statusCode);

    if(statusCode == successStatusCode){
      req.session.isLoggedIn = true;
      req.session.userid = JSON.parse(data).id;
      console.log("user" + req.session.userid);
    }
    else{
     req.session.isLoggedIn = false;
    }
    res.send(statusCode.toString()); 
};

getCallback = function(data,statusCode,req,res){
	console.log(data);
    console.log(statusCode);
    res.send(JSON.stringify(data));
}

postComplaintCallback = function(data,statusCode,req,res){
    console.log(data);
    console.log(statusCode);
    res.send(statusCode.toString()); 
};
var utils = require('./utils');
var session = require('express-session');
var rest_api_url = "https://erqnzqlowa.execute-api.us-west-1.amazonaws.com/Prod";
var rest_helper = require('./rest_helper');
//login url and args
var login_url = rest_api_url + "/login";
var login_args = {
	"email" : "somedude@foobar.com",
	"password" : "password"
}

//parks url
var get_parks_url = rest_api_url + "/parks";


//categories url
var get_categories_url = rest_api_url + "/categories";

var complaints_url = rest_api_url + "/complaints";

var complaint_args = {
      "park": "a2ad0f1d-1c45-4423-9fbe-cd43b3cf2759",
      "user": "0178c1df-b995-4320-b428-ee702bc20d4f",
      "image_url": "url to S3 bucket",
      "description": "This is a sample description",
      "title": "Title Sample",
      "category": "f4d7f5e3-4373-4570-ba0c-ba2c82908609",
      "callback" : "Yes"
    }

module.exports = function(app){
	
	app.use(session({
	    secret: "fd34s@!@dfa453f3DF#$D&W",
	    resave: false,
	    saveUninitialized: true,
	    cookie: { secure: !true }
	}));

    /* GET login page. */
	app.get('/', function(req, res) {
	  res.sendFile('index.html',{"root":"public"});
	});

	/* GET home page. */
	app.get('/home', function(req, res) {
	  utils.redirectToPage("home.html",req,res);
	});

	app.get('/registercomplaint', function(req, res) {
	  utils.redirectToPage("complaint.html",req,res);
	});

	app.get('/park/:id', function(req, res) {
	  utils.redirectToPage("park.html",req,res);
	});

	app.get('/processlogin', function(req, res) {
	   var args = login_args;
	   args.email = req.query.email;
	   args.password = req.query.password;
	   
	   rest_helper.sendRestPostRequest(login_url,args,loginPostCallback,req,res);
	});

	app.get('/getparks', function(req, res) {
	  rest_helper.sendRestGetRequest(get_parks_url,getCallback,req,res);
	});

	app.get('/getcategories', function(req, res) {
	  rest_helper.sendRestGetRequest(get_categories_url,getCallback,req,res);
	});

	app.get('/postcomplaint', function(req, res) {
	  complaint_args.park =  req.query.park;
      complaint_args.user = req.session.userid;
      complaint_args.image_url = "url to S3 bucket";
      complaint_args.description = req.query.description;
      complaint_args.title = req.query.title;
      complaint_args.category = req.query.category;
      complaint_args.callback = req.query.callback;
      console.log("user" + req.session.userid);
	  rest_helper.sendRestPostRequest(complaints_url,complaint_args,postComplaintCallback,req,res);
	});

    //other routes..
}

var utils = require('./utils');
var session = require('express-session');

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
	  req.session.isLoggedIn = true;
	  utils.redirectToPage("home.html",req,res);
	});

	app.get('/processlogin', function(req, res) {
	  var password  = req.query.password;
	  var email = req.query.email;
	  console.log(loginGetUrl+"?email="+email+"&password="+password);
	  sendRestGetRequest(loginGetUrl+"?email="+email+"&password="+password,loginPostCallback,req,res);
	  //loginPostCallback("data",successStatusCode,req,res);
	});

    //other routes..
}
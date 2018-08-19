var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var path = require('path');
require('./routes')(app);

app.use(express.static(path.join(__dirname, 'public')));
app.use(bodyParser.urlencoded({ extended: true })); 

app.use(function(req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
    next();
});

app.listen(3001, function() {
  console.log('Server running at http://127.0.0.1:3001/');
});
var express = require('express');
var http = require('http');
var fs = require('fs');

var app = express();
var server = http.createServer(app);

var firebase = require('firebase');

// See https://firebase.google.com/docs/web/setup#project_setup for how to
// auto-generate this config
var config = {
  apiKey: "AIzaSyDYhRaGOtnjC4JmmgTXag6iBLBlb8MVhQE",
  authDomain: "make-xkcd-great-again.firebaseapp.com",
  databaseURL: "https://make-xkcd-great-again.firebaseio.com"
};

firebase.initializeApp(config);

// TODO add firebase update functions

var rootRef = firebase.database().ref();

// Firebase stuff
var counter = rootRef.child('counter');

app.use(express.static('client'));

app.get('/api/images/:candidate', function(req, res) {
	// get all files
	var path = 'client/img/' + req.params.candidate
	console.log(path)

	fs.readdir(path, function(err, items) {
		console.log(items)
	    res.send(items)
	});
})

app.post('/api/vote', function(req, res) {
	// use req.body.vote to get the person that is getting voted for
});

app.all('/*', function ( req, res ) {
        res.sendFile(__dirname + '/client/index.html');
    })

// make the server start and listen
server.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log("Make XKCD Great Again is running on port " + port);
});
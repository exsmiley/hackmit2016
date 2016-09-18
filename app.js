var express = require('express');
var http = require('http');
var fs = require('fs');

var app = express();
var server = http.createServer(app);

var bodyParser = require('body-parser')
app.use(bodyParser.urlencoded({
  extended: true
}));

var firebase = require('firebase');

// See https://firebase.google.com/docs/web/setup#project_setup for how to
// auto-generate this config
var config = {
  apiKey: "AIzaSyDYhRaGOtnjC4JmmgTXag6iBLBlb8MVhQE",
  authDomain: "make-xkcd-great-again.firebaseapp.com",
  databaseURL: "https://make-xkcd-great-again.firebaseio.com"
};

firebase.initializeApp(config);

var rootRef = firebase.database().ref();

// serve static files
app.use(express.static('client'));

// get all files for the current candidate
app.get('/api/images/:candidate', function(req, res) {
	var path = 'client/img/' + req.params.candidate

	fs.readdir(path, function(err, items) {
	    res.send(items)
	});
})

// updates Firebase with another vote for the candidate that was voted for
app.post('/api/vote', function(req, res) {
  var candidate = req.body.candidate.toLowerCase();

  var counter = rootRef.child('counter');
  counter.child(candidate).once("value", function(snapshot){
    x = snapshot.val();

    if (candidate === "trump") {
      counter.update({"trump": x+1});
    }
    else if (candidate === "hillary") {
      counter.update({"hillary": x+1});
    }
  }); 
});

// have all links direct to our main file
app.all('/*', function ( req, res ) {
        res.sendFile(__dirname + '/client/index.html');
    })

// make the server start and listen
server.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log("Make XKCD Great Again is running on port " + port);
});
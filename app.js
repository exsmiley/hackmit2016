var express = require('express');
var http = require('http');

var app = express();
var server = http.createServer(app);

app.use(express.static('client'));

app.all('/*', function ( req, res ) {
        res.sendFile(__dirname + '/client/index.html');
    })

// make the server start and listen
server.listen(3000, function () {
  var host = server.address().address;
  var port = server.address().port;

  console.log("Make XKCD Great Again is running on port " + port);
});
"use strict";
var express = require('express')
  , routes = require('./routes')
  , http = require('http')
  , path = require('path');

var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 3000);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'ejs');
  app.use(express.favicon());
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);
  app.use(require('less-middleware')(path.join(__dirname, 'public')));
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

app.get('/', routes.index);

var server = http.createServer(app);

var mongoose = require('mongoose');

//connect to localhost node_memo_demo
var db = mongoose.connect('mongodb://localhost/node_memo_demo');
//declare schema in memo
var MemoSchema = new mongoose.Schema({
	text:{type:String}
	,position:{
		left:Number
		,top:Number
	}
});
//generate model from schema
var Memo = db.model('memo',MemoSchema);

server.listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});

var io = require('socket.io').listen(server);

io.sockets.on('connection',function(socket){
	Memo.find(function(err,items){
		if(err){console.log(err);}
		//send memo to user
		socket.emit('create',items);
	});
	//when received create event, add memo to database
	//memoData has type of {text:String,position:{left:Number,top:Number}}
	socket.on('create',function(memoData){
		//make instance from model
		var memo = new Memo(memoData);
		//save to database
		memo.save(function(err){
			if(err){ return; }
			socket.broadcast.json.emit('create',[memo]);
			socket.emit('create',[memo]);
		});
	});
	//when received move event, update Memo's position
	socket.on('move',function(data){
		//search data that matches with _id from database
		Memo.findOne({_id:data._id},function(err,memo){
			if(err || memo === null){return;}
			memo.position = data.position;
			memo.save();
			//send via broadcast to tell the event to another client
			socket.broadcast.json.emit('move',data);
		});
	});
	//when received update-text event, update text in Memo
	socket.on('update-text',function(data){
		Memo.findOne({_id:data._id},function(err,memo){
			if(err || memo === null){return;}
			memo.text = data.text;
			memo.save();
			socket.broadcast.json.emit('update-text',data);
		});
	});
	//when received remove event, delete from database
	socket.on('remove',function(data){
		Memo.findOne({_id:data._id},function(err,memo){
			if(err || memo === null){return;}
			memo.remove();
			socket.broadcast.json.emit('remove',data);
		});
	});
});

/* Chat Server */

var server_port = 8080;
//var http = require('http');
//var server = http.createServer().listen(server_port);
var io = require('socket.io')(server_port);
var async = require('async');
var querystring = require('querystring');
var cookie = require("cookie");
var amqp = require('amqp');
//var utils = require('./utils');

var redis = require('redis');
var client = redis.createClient();

if(!Array.prototype.indexOf) {				  // To handle browsers <= IE8 which do not support 'indexOf' method of Array object.
    Array.prototype.indexOf = function(what, i) {
        i = i || 0;
        var L = this.length;
        while (i < L) {
            if(this[i] === what) return i;
            ++i;
        }
        return -1;
    };
}

Array.prototype.remove = function() {
    var what, a = arguments, L = a.length, ax;
    while (L && this.length) {
        what = a[--L];
        while ((ax = this.indexOf(what)) !== -1) {
            this.splice(ax, 1);
        }
    }
    return this;
};

var sockets = new Object();
var name_enr_map = new Object();
var current_user;


//io.configure(function(){

io.use(function(socket, next){
  console.log(socket);
  //var cookie_manager = cookie.parse(data.headers.cookie);
  //var sid = cookie_manager["sessionid"];
  //console.log(sid);
  next();
  /*
  if(client.get("sid/"+sid), function(error, result){
    if(error){
      console.log("Error: "+error);
    }
    if(result.toString() != ""){
      console.log("Session Active");
      //return accept(null, true);
      next();
      }else{
        console.log("Session Inactive");
      }
  });
  */
  //next(new Error('not authorized');
  //return accept(null, false);
});

/* PRODUCTION LEVEL COFIG SETTINGS */
//io.enable('browser client minification');  // send minified client
//io.enable('browser client etag');          // apply etag caching logic based on version number
//io.enable('browser client gzip');          // gzip the file
//io.set('log level', 1);
//});

/*
io.set('transports', [
     'websocket'
   , 'flashsocket'
   , 'htmlfile'
   , 'xhr-polling'
   , 'jsonp-polling'
]);
*/






function get_friends_online_status(username){
  var OL_friend_status = new Array();
  client.smembers("friends:"+username, function(err, reply){
    for(var i=0; i<reply.length; i++)
    {
      var _status = 0;
      client.hget("user:"+reply[i], "status", function(err, data){
        _status = data;
      });
      OL_friend_status.push({'username': reply[i], 'status': _status, 'last_active': '5min'});
      }
      get_friends_online_status(username, OL_friend_status);
  });
  return OL_friend_status;
}

io.sockets.on('connection', function(socket){
  client.hget("user:11110059", "is_chat_on", function(err, reply){
    if(reply == 1)
    {
      client.hset("user:11110059", "status", 1, function(err, reply){
        console.log(reply);
      });
      console.log("Chat is already on..");
    }
    else
      console.log("Chat is off");
  });
  console.log("socket-id: "+socket.id);

  /*****************************************************************/

  var OL_friend_status = new Array();
  async.series([
  client.smembers("friends:11110059", function(err, reply){
    for(var i=0; i<reply.length; i++)
    {
      client.hget("user:"+reply[i], "status", function(err, _status){
        OL_friend_status.push({'username': reply[i], 'status': _status, 'last_active': '5min'});
        console.log(OL_friend_status);
      });
    }
    console.log(OL_friend_status);
  }),

  //console.log(get_friends_online_status("11110059"));
  //socket.emit("online_users_list", );
  /******************************************************************/

  socket.on("chaton", function(){
    client.hset("user:11110059", "is_chat_on", 1, function(err, reply){
      console.log(reply);
      client.hset("user:11110059", "status", 1, function(err, reply){
        console.log(reply);
      });
    });
  });

  socket.on("chatoff", function(){
    client.hset("user:11110059", "is_chat_on", 0, function(err, reply){
      console.log(reply);
      client.hset("user:11110059", "status", 0, function(err, reply){
        console.log(reply);
      });
    });
  });

  socket.on('disconnect', function(){
    client.hset("user:11110059", "status", 0, function(err, reply){
      console.log(reply);
    });
    console.log(socket.id+" is disconnected");
  });
});


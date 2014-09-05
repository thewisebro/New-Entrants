/* Chat Server */

var server_port = 8088;
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

var _sockets = new Object();
var name_enr_map = new Object();
var sid;

io.use(function(socket, next){
  var cookie_manager = cookie.parse(socket.handshake.headers.cookie);
  sid = cookie_manager["PHPSESSID"];
  console.log("\n\n<----------------------------------------------------------->");
  console.log(sid);
  client.get("session:"+sid, function(error, result){
    if(error){
      console.log("Error: "+error);
    }
    else if(result != null){
      console.log("Session Active");
      socket.user = JSON.parse(result);
      next();
    }
    else{
      console.log("Session Inactive");
    }
  });
  next(new Error('not authorized'));
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

io.on('connection', function(socket){
  var current_user = new Object();
  current_user = socket.user;
  console.log(current_user);

  client.hget("user:" + current_user.user_id, "is_chat_on", function(err, reply){
    if(reply == 1)
    {
      client.hset("user:" + current_user.user_id, "status", 1, function(err, reply){
        current_user.status = 1;

        if(current_user.user_id in _sockets)
        {
          _sockets[ current_user.user_id ].push(socket.id);
        }
        else
        {
          _sockets[ current_user.user_id ] = new Array();
          _sockets[ current_user.user_id ].push(socket.id);
        }
        console.log(_sockets);
      });
      console.log("Chat is already on..");
    }
    else
      console.log("Chat is off");
  });
  console.log("socket-id: "+socket.id);

  /*****************************************************************/

  client.smembers("friends:" + current_user.user_id, function(err, items){
    var OL_friend_status = new Array();
    async.eachSeries(items,
      function(item, callback){
        client.hgetall("user:"+item, function(err, data){
          OL_friend_status.push(data);
          callback();
        });
      },
      function(err){
        if(err){
          console.log("Error occured!");
        } else{
          async.parallel([
            (function(){  // Function-1
              var json_payload = {'friends': OL_friend_status};
              socket.emit("friends_list", json_payload);
            })(),
            send_conn_status( OL_friend_status )  // Function-2
          ],
          function(err, results){
            console.log("Task Done.");
          });
        }
      }
    );
  });
  /******************************************************************/

  socket.on("chaton", function(){
    console.log("IN CHATON");
    client.hmset("user:"+current_user.user_id, {"is_chat_on": 1, "status": 1}, function(err, reply){
      propogate_chat_status("chat_on");
    });
  });

  socket.on("chatoff", function(){
    console.log("IN CHATOFF");
    client.hmset("user:"+current_user.user_id, {"is_chat_on": 0, "status": 0}, function(err, reply){
      propogate_chat_status("chat_off");
    });
  });

  socket.on('disconnect', function(){
    console.log(socket.id+" is disconnected");
    if(current_user.user_id in _sockets)
    {
      _sockets[ current_user.user_id ].remove(socket.id);
      console.log(_sockets);
      if(_sockets[current_user.user_id].length == 0)
      {
        client.hset("user:"+current_user.user_id, "status", 0, function(err, reply){
          current_user.status = 0;
          send_disconn_status(); // Here argument '0' is the current user status.
        });
      }
     }
  });


/* FUNCTIONS MODULE */
function propogate_chat_status( chat_status ) // Handles both "chat_on" and "chat_off" status.
{
  var current_user_status = {"chat_on": 1, "chat_off": 0};
  client.smembers("friends:" + current_user.user_id, function(err, items){
    if(err){
      console.log("Error occured!");
    }
    else
    {
       /* TASK-1 */
       if(chat_status == "chat_on")
       {
         var OL_friend_status = new Array();
         async.eachSeries(items,
           function(item, callback){
            client.hgetall("user:"+item, function(err, data){
              OL_friend_status.push(data);
              callback();
            });
           },
           function(err){
             if(err){
              console.log("Error occured!");
             }
             else
             {
               for(var _counter_1=0; _counter_1< OL_friend_status.length; _counter_1++)
               {
                  var item = items[_counter_1];
                  client.hgetall("user:"+item, function(err, data){
                    if(_sockets[current_user.user_id] != undefined)
                    {
                      for(var _counter_1=0; _counter_1<_sockets[current_user.user_id]; _counter_1++)
                      {
                        var _sock = _sockets[current_user.user_id][_counter_1];
                        io.to(_sock).emit("friends_list", {"friends": OL_friend_status});
                      }
                    }
                  });
               }
             }
           }
         );
       }
       /* ENDS */

       /* TASK-2 */
       for(var k=0; k<items.length; k++)
       {
          var friend_id = items[k];
          var friend_socks = new Array();
          if(_sockets[friend_id] != undefined)
          {
            friend_socks = _sockets[friend_id];
            for(var _counter_2=0; _counter_2<friend_socks.length; _counter_2++)
            {
              var _sock = friend_socks[_counter_2];
              io.to(_sock).emit("update_friend_status", {"user_id": current_user.user_id, "status": current_user_status[chat_status] });
              console.log("Friend status update sent.");
            }
          }
          else
            continue;
       }
       /* ENDS */
    }
  });
}

function send_conn_status(ou_list) // Function to send friend status update in OU list.
{
  var _status = 1;
  for(var _counter_1=0; _counter_1<ou_list.length; _counter_1++)
  {
      var friend_id = ou_list[_counter_1]["user_id"];
      var friend_socks = new Array();
      if(_sockets[friend_id] != undefined)
      {
        friend_socks = _sockets[friend_id];
        for(var _counter_2=0; _counter_2<friend_socks.length; _counter_2++)
        {
          var _sock = friend_socks[_counter_2];
          io.to(_sock).emit("update_friend_status", {"user_id": current_user.user_id, "status": _status});
          console.log("Conn status update sent.");
        }
      }
      else
        continue;
  }
}

function send_disconn_status() // Function to send friend status update in OU list.
{
  var _status = 0;
  client.smembers("friends:" + current_user.user_id, function(err, items){
    if(err){
      console.log("Error occured!");
    } else{
        for(var k=0; k<items.length; k++)
        {
          var friend_id = items[k];
          var friend_socks = new Array();
          if(_sockets[friend_id] != undefined)
          {
            friend_socks = _sockets[friend_id];
            for(var _counter=0; _counter<friend_socks.length; _counter++)
            {
              var _sock = friend_socks[_counter];
              io.to(_sock).emit("update_friend_status", {"user_id": current_user.user_id, "status": _status});
              console.log("Disconn status update sent.");
            }
          }
          else
            continue;
        }
    }
  });
}
/* FUNCTIONS MODULE ENDS */

});

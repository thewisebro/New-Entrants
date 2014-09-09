var socket;
var document_state_var = 0;
//$(document).ready(function(){
//});

//localStorage.debug = '*';

$(document).on("pagelet_loaded_header_sidebar",function(){
  if(user.is_authenticated && document_state_var == 0){
    console.log("Already logged in....");
    chat_connect();
  }
});

$(document).on("login", function(){
  load_pagelet("header_sidebar");
  $(window).scrollTop(0);
  console.log("Login fired...");
  chat_connect();
  document_state_var = 1;
});

$(document).on("logout", function(){
  load_pagelet("header_sidebar");
  $(window).scrollTop(0);
  console.log("Logout fired...!");
  chat_disconnect();
});

function chat_connect(){
  var options = new Object();
  options['force new connection'] = true;
  socket = io.connect('http://192.168.121.5:8088', options);
  socket.on('connect', function(){
    console.log("connected....");
  });

  socket.on("update_friend_status", function(_friend){
      var status_color = {"1": "green", "0": "grey"};
      console.log("UPDATE friend status");
      console.log(_friend);
      if($("#online-user_"+_friend.user_id) != undefined)
      {
        $("#online-user_"+_friend.user_id).children(".ou-status").css("background-color", status_color[_friend.status]);
      }
      //JSON.parse(json_payload);
  });

  socket.on('friends_list', function(json_payload){
    console.log(json_payload);
    var friends = json_payload["friends"];
    var status_color = {"1": "green", "0": "grey"};
    var ol_users = "";
    for(var i=0; i<friends.length; i++)
    {
      var online_user = ""+
        "<div class='online-user' id='online-user_"+ friends[i].user_id +"'>"+
          "<div class='ou-image'>"+
          "<img src='"+ friends[i].photo+"'>"+
          "</div>"+
          "<div class='ou-name'>"+
          friends[i].name+
          "</div>";
          if(friends[i].status == 1)
          {
            online_user += "<div class='ou-status' style='background-color:green;'>"+
                            "</div>";
          }
          else
          {
            online_user += "<div class='ou-status' style='background-color:grey;'>"+
                            "</div>";
          }
          online_user += "<div style='clear:both;'></div>"+
                         "</div>";
       ol_users += online_user;
    }
    $(".online-users").html(ol_users);

  });
}

function chat_reconnect(){
  socket.socket.reconnect();
  //socket = "";
}

function chat_disconnect(){
  socket.disconnect();
  //socket = "";
}

function chaton()
{
  console.log("In chaton");
  socket.emit("chaton", function(){
    console.log("chat -> on");
  });
}
function chatoff()
{
  console.log("In chatoff");
  socket.emit("chatoff", function(){
    console.log("chat -> off");
  });
}

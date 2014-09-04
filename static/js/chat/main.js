var socket;
$(document).ready(function(){
  //function connect(){
    socket = io.connect('http://192.168.121.5:8080');
    socket.on('connect', function(){
      console.log("connected....");
    });
  //}
});

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


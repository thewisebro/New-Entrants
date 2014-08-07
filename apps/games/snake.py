from games.canvasgame import CanvasGame

timeinterval = 15

#ESCAPE = 27;
#ENTER = 13;
#SPACE = 32;
#UP = 38;
#LEFT = 37;
#RIGHT = 39;
#DOWN = 40;
#KEY_W = 87;
#KEY_A = 65;
#KEY_D = 68;


htmlbody = r"""
<div id="game" style="width:800px;margin:10px auto 0px auto;color:#acacac;font-family:sans-serif;"></div>
 <script type="text/javascript" src="/static/js/games/easel.js"></script>
"""

# init called once
init = r"""
A.MAXSPEED = 3;
A.speed=1;

A.handleKeyDown = function(e) {
if(!e){ var e = window.event; }
switch(e.keyCode) {
case 27:    A.key.esc = true;break;
case 13:     A.key.enter = true; break;
case 32:	A.key.space = true; break;
case 37:	A.key.left = true; break;
case 39:     A.key.right = true; break;
case 38:	A.key.up = true; break;
case 40:	A.key.down = true; break;
}
};
A.handleKeyUp = function(e) {
if(!e){ var e = window.event; }
switch(e.keyCode) {
case 27:    A.key.esc = false;break;
case 13:     A.key.enter = false; break;
case 32:	A.key.space = false; break;
case 37:	A.key.left = false; break;
case 39:     A.key.right = false; break;
case 38:	A.key.up = false; break;
case 40:	A.key.down = false; break;
}
};
A.bitShape = function()
{var s = new Shape();
 s.graphics.beginStroke("000");
 s.graphics.beginFill("#ff8").drawRoundRect(0,0,10,10,2);
 s.cache(0,0,10,10);
 return s;
};
A.foodShape = function()
{var s = new Shape();
 s.graphics.beginStroke("f22");
 s.graphics.beginFill("#f22").drawRoundRect(0,0,10,10,2);
 s.cache(0,0,10,10);
 return s;
};
A.random = function(x)
{return parseInt(""+Math.random()*x);
};

A.check = function(x,y){
for(var i=0;i<A.snake.length-1;i++){
if(A.snake[i].s.x==x&&A.snake[i].s.y==y)
return true;
}
return false; 
};

A.randomizefood=function(){
do{
A.food.x = A.random(A.c.width/10)*10;
A.food.y = A.random(A.c.height/10)*10;
}while(A.check(A.food.x,A.food.y));
};

document.getElementById("game").innerHTML = "
<button id='start'><h2>Start</h2></button> the Snake game.";
document.getElementById("start").onclick = function(){A.tostart=true;};


"""

# start called repeatedly unless A.started is set true.
start = r"""
if(A.tostart){
document.getElementById("game").innerHTML = '
<canvas id="canvas" width="800px" height="400px" 
 style="margin:0px auto;padding:0px;background:#000;border:2px solid brown;"></canvas>
 <div id="snake_score" style="width:100px;color:#fff;"></div>
';
A.count=0;
A.key=[];
A.snake=[];
document.onkeydown = A.handleKeyDown;
document.onkeyup = A.handleKeyUp;
A.c = document.getElementById("canvas");
A.stage = new Stage(A.c);
A.cover = new Shape();
A.stage.addChild(A.cover);
A.stage.autoClear = true;
A.snake.push([]);
A.snake[0].s = A.bitShape();
A.snake[0].s.x = A.c.width/2;
A.snake[0].s.y = A.c.height/2;
A.snake[0].d = A.random(4);
A.stage.addChild(A.snake[0].s);
A.food = A.foodShape();
A.randomizefood();
A.stage.addChild(A.food);
A.started = true;
}
"""

# paint called repeatedly unless A.stop is set true
paint = r"""
A.count+=A.speed;if(A.count>=A.MAXSPEED){
var dx=0,dy=0;
switch(A.snake[0].d){
case 0:dx=10;break;
case 1:dy=10;break;
case 2:dx=-10;break;
case 3:dy=-10;break;
}
var nx=A.snake[0].s.x+dx,ny=A.snake[0].s.y+dy;

if(A.check(nx,ny)){A.stop = true;}
if(nx<0 || nx>=A.c.width || ny<0 || ny>=A.c.height){A.stop = true;}
/*if(nx<0){nx+=A.c.width;}
if(nx>=A.c.width){nx=A.c.width-nx;}
if(ny<0){ny+=A.c.height;}
if(ny>=A.c.height){ny=A.c.height-ny;}*/


if(nx==A.food.x&&ny==A.food.y)
{A.randomizefood();
 var newhead = [];
 newhead.s = A.bitShape();
 newhead.s.x=nx;
 newhead.s.y=ny;
 newhead.d = A.snake[0].d;
 A.snake = [newhead].concat(A.snake);
 A.stage.addChild(A.snake[0].s);
 A.score+=A.speed;
}
else{
if(A.snake.length==1){
A.snake[0].s.x=nx;
A.snake[0].s.y=ny;
}
else{
var l = A.snake.length;
var last = A.snake[l-1];
A.snake = [last].concat(A.snake.slice(0,l-1));
A.snake[0].d = A.snake[1].d;
A.snake[0].s.x=nx;
A.snake[0].s.y=ny;
}
}
A.count-=A.MAXSPEED;
}
A.speed=1+0.2*parseInt(A.snake.length/10);
if(A.speed>A.MAXSPEED)A.speed=A.MAXSPEED;
var d;
if(A.key.right){d=0;}
else if(A.key.down){d=1;}
else if(A.key.left){d=2;}
else if(A.key.up){d=3;}
if(d!=undefined&&Math.abs(d-A.snake[0].d)!=2){A.snake[0].d=d;}
if(!A.stop)
{A.stage.update();
}
document.getElementById("snake_score").innerHTML="Score : "+parseInt(A.score);
"""

# called once as A.stop is set true
stop = r"""
   document.getElementById("canvas").style.display="None";
   setTimeout(function(){location="";},2000); 
"""

game = CanvasGame(gamecode='snake',gamename="Snake",htmlbody=htmlbody,init=init,start=start,paint=paint,stop=stop,timeinterval=timeinterval)
game.register()

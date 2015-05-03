from games.canvasgame import CanvasGame

timeinterval = 100

htmlbody = r"""
<div id="game" style="width:500px;height:350px;margin:10px auto;color:#fff;"></div>
"""

# init called once
init = r"""
document.getElementById("game").style.height="200px";
document.getElementById("game").innerHTML = "How fast you can click the mouse !<br>"+
"<button id='start'>Start</button>";
document.getElementById("start").onclick = function(){A.tostart=true;};
"""

# start called repeatedly unless A.started is set true.
start = r"""
if(A.tostart){
document.body.onclick = function(){if(A.score<250)A.score++;};
A.time=0;
A.started = true;
}
"""

# paint called repeatedly unless A.stop is set true.
paint = r"""
A.time++;
document.getElementById("game").innerHTML = "Time Left : "+(20-Math.round(A.time/10,0))+"<br>Score : "+A.score;
if(A.time>200){A.stop = true;}
"""

# stop called once as A.stop is set true.
stop = r"""
document.getElementById("game").innerHTML="Your score is "+A.score;
setTimeout(function(){location="";},1000);
"""

game = CanvasGame(gamecode='mouseclick',gamename="Mouse Click",htmlbody=htmlbody,init=init,start=start,paint=paint,stop=stop,timeinterval=timeinterval)
game.register()

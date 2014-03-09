from games.canvasgame import CanvasGame

timeinterval = 100

htmlbody = r"""
<div id="game">
  <link href="/static/css/games/sinuous/styles.css" rel="stylesheet" media="screen" />
  <div id="status" class="ui"></div>
  <div id="panels">
    <div id="message" class="ui">
      <h2 id="title">Sinuous</h2>
      <ul>
        <li>1. Avoid red dots.</li>
        <li>2. Touch green dots for invulnerability.</li>
        <li>3. Use invulnerability to destroy red dots.</li>
        <li>4. Score extra points by moving around a lot.</li>
        <li>5. Stay alive.</li>
      </ul>
      <a href="#" id="startButton">Start</a>
    </div>
    <div id="highscoreWin" class="ui">
      <h2 id="highscorePlace"></h2>
      <p>Something to identify you by</p>
      <input id="highscoreInput" type="text" name="alias" maxlength="10" />
      <a id="highscoreSubmit" href="#">Go</a>
    </div>
  </div>

  <div id="seeMore"></div>
  <script>var sc = 6743;</script>
  <canvas id="world"><p class="noCanvas">You need a <a href="http://www.google.com/chrome">modern browser</a> to view this.</p></canvas>
  <div id="submit"><div>
  <script src="/static/js/games/sinuous/sinuous.min.js"></script>
</div>
"""

init=r"""
A.s = SinuousWorld(A);
A.s.init();
"""
  
stop=r"""
delete A.s;
var newhtml = "<div style='margin:0px auto;width:200px;color:#fff;'>"+"You scored "+A.score+ "</div>";
document.getElementById("game").innerHTML=newhtml;
setTimeout(function(){location="";},3000);
"""

game = CanvasGame(gamecode='sinuous',gamename="Sinuous",htmlbody=htmlbody,init=init,stop=stop,timeinterval=timeinterval)
game.register()

from games.canvasgame import CanvasGame

timeinterval = 100

htmlbody = r"""
    <style type="text/css">
       * { margin:0px; padding:0px; }
       #helicopter { margin: 10px 0px; font-family:SilkScreenBold; }
       html.wf-silkscreen-n4-active body { visibility:visible; }
    </style>
  <span style="font-family:SilkScreenBold;"> </span>

  <div id="helicopter" style="width:600px;height:auto;margin:0px auto;"></div>

  <script src="/static/js/games/helicopter/helicopter.js"></script>
  <script src="/static/js/games/helicopter/modernizr-1.5.min.js"></script>
  <script src="/static/js/games/helicopter/webfont.js"></script>
 """

# init called once
init = r"""
A.s = game(A);
A.s();
w();
"""

# start called repeatedly unless A.started is set true.
start = r"""
"""

# paint called repeatedly unless A.stop is set true.
paint = r"""
"""

# stop called once as A.stop is set true.
stop = r"""
  setTimeout(function(){location="";},1000);
"""

game = CanvasGame(gamecode='helicopter',gamename="Helicopter",htmlbody=htmlbody,init=init,start=start,paint=paint,stop=stop,timeinterval=timeinterval)
game.register()

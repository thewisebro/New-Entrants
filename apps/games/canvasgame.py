from django.template import Context, Template

def escape(s):
  return s.replace('\\','\\\\').replace('\'','\\\'').replace('\"','\\\"')

raw_html = """
 <!--htmlbody-->
 <script type="text/javascript">
 <!--script-->
 </script>
"""  

scriptmid = r"""
function(){
var A;
if(!arguments.length){A=arguments.callee;
A._iter=setInterval(A,<!--timeinterval-->,A);
A.gsession="<!--gsession-->";A._authenticated=false;A._init=false;A.started=false;A.stop=false;A._t=0;A.score=0;

A.strescape = function(str){
var s=str.replace(/\\/g,'\\\\').replace(/\"/g,'\\\"').replace(/\'/g,'\\\'');
return s;
};

A.getXHRObject = function(func){
var xhr;
if(window.XMLHttpRequest)
xhr = new XMLHttpRequest();
else if(window.ActiveXObject)
xhr = new ActiveXObject("Microsoft.XMLHTTP");
xhr.onreadystatechange = function()
{if(xhr.readyState==4 && xhr.status==200 && func!=undefined)
func(xhr);
};
return xhr;
};
}
else{A=arguments[0];
}

A._t++;
if(A._authenticated){if(!A._init){<!--init-->A._init=true;}else{if(!A.started){<!--start-->}else{<!--paint-->}}
if(A.stop){<!--stop-->}}

if(!A._authenticated && A._t==2){
var xhr = A.getXHRObject(function(xhr){
A.auth = xhr.responseText;
if(A.auth){A._authenticated=true;}
else A.stop = true;
});
xhr.open("POST","authenticate/",true);
xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xhr.send("wow="+escape(A.toString())+"&gsession="+A.gsession);
}

if(A.stop){
var xhr = A.getXHRObject();
xhr.open("POST","stop/",true);
xhr.setRequestHeader("Content-type","application/x-www-form-urlencoded");
xhr.send("wow="+escape(A.toString())+"&gsession="+A.gsession+"&auth="+A.auth+"&t="+A._t+"&s="+A.score);
clearInterval(A._iter)
}
}
"""

script=r"""
("""+scriptmid+r""")()
"""

class CanvasGame(object):
  registered_games = {}
  def __init__(self,gamecode,gamename,htmlbody="",init="",start="",paint="",stop="",timeinterval=10):
    self.gamecode = gamecode
    self.gamename = gamename
    self.htmlbody = htmlbody
    self.init = init
    self.start = start
    self.paint = paint
    self.stop = stop
    self.timeinterval = timeinterval

  
  def register(self):
    CanvasGame.registered_games[self.gamecode]=self;
    
  def html(self,gsession):
    finalscript = script.replace("<!--init-->",self.init)
    finalscript = finalscript.replace("<!--start-->",self.start)
    finalscript = finalscript.replace("<!--paint-->",self.paint)
    finalscript = finalscript.replace("<!--stop-->",self.stop)
    finalscript = finalscript.replace("<!--timeinterval-->",str(self.timeinterval))
    finalscript = finalscript.replace("<!--gsession-->",gsession)
    html = raw_html.replace("<!--htmlbody-->",self.htmlbody)
    html = html.replace("<!--script-->",finalscript.replace('\n',''))
    t = Template(html)  
    c = Context({})
    return t.render(c)
   

  @staticmethod  
  def getGame(gamecode):
    return CanvasGame.registered_games[gamecode]

  def is_same(self,gsession,code):
    midscript = scriptmid.replace("<!--init-->",self.init)
    midscript = midscript.replace("<!--start-->",self.start)
    midscript = midscript.replace("<!--paint-->",self.paint)
    midscript = midscript.replace("<!--stop-->",self.stop)
    midscript = midscript.replace("<!--timeinterval-->",str(self.timeinterval))
    midscript = midscript.replace("<!--gsession-->",gsession)  
    midscript = midscript.replace('\n','').replace(' ','').replace('+','')
    code = code.replace('\n','').replace(' ','').replace('+','')
    return midscript==code
  
import games.mouseclick
import games.snake
import games.sinuous
import games.helicopter

function loadScript(sScriptSrc,callbackfunction) 
{
  //gets document head element
  var oHead = document.getElementsByTagName('head')[0];
  if(oHead)
  {
    //creates a new script tag    
    var oScript = document.createElement('script');

    //adds src and type attribute to script tag
    oScript.setAttribute('src',sScriptSrc);
    oScript.setAttribute('type','text/javascript');

    //calling a function after the js is loaded (IE)
    var loadFunction = function()
    {
      if (this.readyState == 'complete' || this.readyState == 'loaded')
      {
        callbackfunction(); 
      }
    };
    oScript.onreadystatechange = loadFunction;

    //calling a function after the js is loaded (Firefox)
    oScript.onload = callbackfunction;

    //append the script tag to document head element    
    oHead.appendChild(oScript);
  }
}

function remove_spare_cookies(){
  var cookies = document.cookie.split(';');
  var cookies_to_remove = cookies.filter(function(c){var i=c.substr(0,6); return (i=='_pk_id' || i==' _pk_i');}).map(function(c){return c.split('=')[0];});
  function deleteCookie(cookiename){
    var d = new Date();
    d.setDate(d.getDate() - 1);
    var expires = ";expires="+d;
    var name=cookiename;
    var value="";
    document.cookie = name + "=" + value + expires + "; path=/";
  }
  if(cookies_to_remove.length > 1)
    cookies_to_remove.map(function(c){deleteCookie(c);});
}

(function(){
  // first matched url will get preference.
  var url_piwikid_map = {
    '^/placement/':2,
    '^/lectut/':3,
    '^/thinktank/':4,
    '^/lostfound/':5,
    '^/softwares/':7,
    '^/messmenu/':8,
    '^/research_assistant/':9,
    '^/helpcenter/':10,
    '^/settings/':11,
    '^/PeopleSearch/':12,
    '^/games/':13,
    '^/groups/':14,
    '^/facapp/':15,
    '^/notices/':16,
    '^/yaadein/':17,
    '^/buysell/':18,
    '^/connect-e-dil/':20,
    '^/get-app/':21,
    '^/$':1,
  };
  remove_spare_cookies();
  var urls = Object.keys(url_piwikid_map).filter(function(url){return document.location.pathname.search(url) != -1;});

  var analytics_location = (location.host == 'people.iitr.ernet.in') ? 'people.iitr.ernet.in/piwik/' : 'channeli.in/piwik/';

  if(urls.length){
    var piwikid = url_piwikid_map[urls[0]];
    var pkBaseURL = (("https:" == document.location.protocol) ? ("https://"+analytics_location) : ("http://"+analytics_location));
    loadScript(pkBaseURL+"piwik.js",function(){
        var piwikTracker = Piwik.getTracker(pkBaseURL + "piwik.php",piwikid);
        if(piwikid==1)
          piwikTracker.setCookiePath('/');
        else
          piwikTracker.setCookiePath(urls[0].substr(1));
        piwikTracker.trackPageView();
        piwikTracker.enableLinkTracking();
    });
  }
})();
